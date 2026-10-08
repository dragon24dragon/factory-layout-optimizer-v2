import { describe, expect, it } from "vitest";
import fixtures from "./__fixtures__/python_results.json";
import {
  generateRankedLayouts,
  resolveUnits,
  totalWeightedFlowDistance,
  type Area,
  type Layout,
} from "./layout";
import { areas, dailyFlows, factory } from "./sampleData";

const unit = (id: string, x: number, y: number) => ({
  area: { id, name: id, count: 1, widthM: 2, heightM: 2 } as Area,
  xM: x,
  yM: y,
});

describe("Python 版と同じ答えになる", () => {
  for (const c of fixtures.cases) {
    const label = `候補数${c.candidate_count}・外壁${c.wall}m・間隔${c.gap}m`;

    it(label, () => {
      const run = () =>
        generateRankedLayouts(factory, areas, dailyFlows, c.candidate_count, c.wall, c.gap);

      if ("error" in c && c.error) {
        expect(run).toThrow(c.error);
        return;
      }

      const ranked = run();
      expect(ranked.map((r) => r.candidateId)).toEqual(c.ranking!.map((r) => r.candidate_id));

      ranked.forEach((r, i) => {
        const expected = c.ranking![i];
        expect(r.score).toBeCloseTo(expected.score, 9);

        const positions = Object.fromEntries(
          Object.entries(r.layout).map(([id, p]) => [id, [p.xM, p.yM]]),
        );
        expect(positions).toEqual(expected.positions);
      });
    });
  }
});

describe("搬送回数の数え方", () => {
  it("台が複数あるときは回数を均等に割り振る", () => {
    const layout: Layout = {
      source: unit("source", 0, 0),
      machine_1: unit("machine_1", 3, 4),
      machine_2: unit("machine_2", 6, 8),
    };
    // 30回を2台に15回ずつ：5m × 15回 ＋ 10m × 15回
    expect(
      totalWeightedFlowDistance(layout, [{ from: "source", to: "machine", trips_per_day: 30 }]),
    ).toBe(225);
  });

  it("似た名前の設備を混ぜない", () => {
    const layout: Layout = {
      machine_1: unit("machine_1", 0, 0),
      machine_big_1: unit("machine_big_1", 30, 40),
    };
    expect(resolveUnits("machine", layout).map((u) => u.area.id)).toEqual(["machine_1"]);
  });

  it("サンプルデータの10区間がすべて計算に入る", () => {
    const [{ layout }] = generateRankedLayouts(factory, areas, dailyFlows, 1);
    for (const flow of dailyFlows) {
      expect(resolveUnits(flow.from, layout).length, flow.from).toBeGreaterThan(0);
      expect(resolveUnits(flow.to, layout).length, flow.to).toBeGreaterThan(0);
    }
  });
});
