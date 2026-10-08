// 配置の生成と採点。Python 版（layout_optimizer/）を TypeScript に移したもの。
// 計算結果は Python 版と一致することを layout.test.ts で確かめている。

export type Factory = {
  widthM: number;
  heightM: number;
};

export type Area = {
  id: string;
  name: string;
  count: number;
  widthM: number;
  heightM: number;
};

export type PlacedArea = {
  area: Area;
  xM: number;
  yM: number;
};

export type Layout = Record<string, PlacedArea>;

export type DailyFlow = {
  from: string;
  to: string;
  trips_per_day: number;
};

export type RankedCandidate = {
  candidateId: number;
  score: number;
  layout: Layout;
};

// 台数ぶんに展開する。例：切断機（2台）→ 切断機1・切断機2
export function expandAreas(areas: Area[]): Area[] {
  const expanded: Area[] = [];

  for (const area of areas) {
    for (let index = 0; index < area.count; index++) {
      const single = area.count === 1;

      expanded.push({
        id: single ? area.id : `${area.id}_${index + 1}`,
        name: single ? area.name : `${area.name}${index + 1}`,
        count: 1,
        widthM: area.widthM,
        heightM: area.heightM,
      });
    }
  }

  return expanded;
}

// 左下から右へ並べ、はみ出しそうなら次の段へ送る。
// 引数の areas は展開前でも展開後でもよい（展開後なら台数はすべて1）。
export function generateGridLayout(
  factory: Factory,
  areas: Area[],
  wallClearanceM = 1.0,
  gapM = 2.0,
): Layout {
  const placed: Layout = {};

  let currentX = wallClearanceM;
  let currentY = wallClearanceM;
  let rowHeight = 0;

  const usableRight = factory.widthM - wallClearanceM;
  const usableTop = factory.heightM - wallClearanceM;

  for (const area of expandAreas(areas)) {
    if (currentX + area.widthM > usableRight) {
      currentX = wallClearanceM;
      currentY += rowHeight + gapM;
      rowHeight = 0;
    }

    if (currentY + area.heightM > usableTop) {
      throw new Error(
        `${area.name}を配置できません。工場内のスペースが不足しています。`,
      );
    }

    placed[area.id] = { area, xM: currentX, yM: currentY };

    currentX += area.widthM + gapM;
    rowHeight = Math.max(rowHeight, area.heightM);
  }

  return placed;
}

// 並べる順番を1つずつずらして、候補を作る。
export function generateCandidateLayouts(
  factory: Factory,
  areas: Area[],
  candidateCount = 5,
  wallClearanceM = 1.0,
  gapM = 2.0,
): Layout[] {
  if (candidateCount <= 0) return [];

  const expanded = expandAreas(areas);
  if (expanded.length === 0) return [];

  const layouts: Layout[] = [];
  const variations = Math.min(candidateCount, expanded.length);

  for (let shift = 0; shift < variations; shift++) {
    const reordered = [...expanded.slice(shift), ...expanded.slice(0, shift)];
    layouts.push(generateGridLayout(factory, reordered, wallClearanceM, gapM));
  }

  return layouts;
}

export function centerOfArea(placed: PlacedArea): [number, number] {
  return [
    placed.xM + placed.area.widthM / 2,
    placed.yM + placed.area.heightM / 2,
  ];
}

export function centerDistance(first: PlacedArea, second: PlacedArea): number {
  const [x1, y1] = centerOfArea(first);
  const [x2, y2] = centerOfArea(second);

  return Math.hypot(x2 - x1, y2 - y1);
}

// 搬送回数の表は「台数で分ける前の名前」で書かれている。
// 例：cutting_machine → cutting_machine_1 と cutting_machine_2
// 「A_or_B」は「AかB」の意味で、両方の台をまとめて返す。
export function resolveUnits(flowId: string, layout: Layout): PlacedArea[] {
  if (flowId in layout) return [layout[flowId]];

  const units: PlacedArea[] = [];

  for (const part of flowId.split("_or_")) {
    if (part in layout) {
      units.push(layout[part]);
      continue;
    }

    const prefix = part + "_";

    for (const [areaId, placed] of Object.entries(layout)) {
      const suffix = areaId.slice(prefix.length);

      if (areaId.startsWith(prefix) && /^\d+$/.test(suffix)) {
        units.push(placed);
      }
    }
  }

  return units;
}

// 距離 × 1日の搬送回数 の合計。小さいほど良い。
// 台が複数あるときは、回数をすべての組み合わせに均等に割り振る。
export function totalWeightedFlowDistance(
  layout: Layout,
  dailyFlows: DailyFlow[],
): number {
  let total = 0;

  for (const flow of dailyFlows) {
    const fromUnits = resolveUnits(flow.from, layout);
    const toUnits = resolveUnits(flow.to, layout);

    if (fromUnits.length === 0 || toUnits.length === 0) continue;

    const pairCount = fromUnits.length * toUnits.length;

    for (const fromUnit of fromUnits) {
      for (const toUnit of toUnits) {
        total += centerDistance(fromUnit, toUnit) * (flow.trips_per_day / pairCount);
      }
    }
  }

  return total;
}

export function rankCandidateLayouts(
  layouts: Layout[],
  dailyFlows: DailyFlow[],
): RankedCandidate[] {
  const ranked = layouts.map((layout, index) => ({
    candidateId: index + 1,
    score: totalWeightedFlowDistance(layout, dailyFlows),
    layout,
  }));

  // 同点のときは元の候補番号の順（Python の sort と同じく安定）
  return ranked.sort((a, b) => a.score - b.score);
}

export function generateRankedLayouts(
  factory: Factory,
  areas: Area[],
  dailyFlows: DailyFlow[],
  candidateCount = 5,
  wallClearanceM = 1.0,
  gapM = 2.0,
): RankedCandidate[] {
  const layouts = generateCandidateLayouts(
    factory,
    areas,
    candidateCount,
    wallClearanceM,
    gapM,
  );

  return rankCandidateLayouts(layouts, dailyFlows);
}
