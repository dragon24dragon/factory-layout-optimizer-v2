import type { Factory, Layout } from "@/lib/layout";

// 配置図。工場を真上から見た図で、左下が原点 (0, 0)。
// SVG は上が y=0 なので、上下を反転して描く。

const BASE_IDS = [
  "raw_material_storage",
  "cutting_machine",
  "machining_center",
  "lathe",
  "welding_area",
  "wip_storage",
  "inspection_area",
  "packing_area",
  "finished_goods_storage",
  "shipping_area",
];

function colorIndex(areaId: string): number {
  const base = areaId.replace(/_\d+$/, "");
  const index = BASE_IDS.indexOf(base);
  return index === -1 ? 0 : index;
}

export default function LayoutChart({
  factory,
  layout,
  title,
}: {
  factory: Factory;
  layout: Layout;
  title: string;
}) {
  const pad = 4;
  const { widthM: w, heightM: h } = factory;
  const flipY = (y: number) => h - y;

  const ticks: number[] = [];
  for (let t = 0; t <= Math.max(w, h); t += 10) ticks.push(t);

  return (
    <figure className="chart">
      <svg
        viewBox={`${-pad} ${-pad} ${w + pad * 2} ${h + pad * 2}`}
        role="img"
        aria-label={title}
      >
        <rect x={0} y={0} width={w} height={h} className="chart-floor" />

        {ticks.map((t) => (
          <g key={t}>
            {t <= w && (
              <>
                <line x1={t} y1={0} x2={t} y2={h} className="chart-grid" />
                <text x={t} y={h + 2.6} className="chart-tick" textAnchor="middle">
                  {t}
                </text>
              </>
            )}
            {t <= h && (
              <>
                <line x1={0} y1={flipY(t)} x2={w} y2={flipY(t)} className="chart-grid" />
                <text x={-1} y={flipY(t) + 0.6} className="chart-tick" textAnchor="end">
                  {t}
                </text>
              </>
            )}
          </g>
        ))}

        {Object.entries(layout).map(([id, placed]) => {
          const { area } = placed;
          const x = placed.xM;
          const y = flipY(placed.yM + area.heightM);
          // 1行で小さくなりすぎる名前は、2行に折り返す（例：マシニング／センタ1）
          const oneLineSize = (area.widthM * 0.9) / area.name.length;
          const half = Math.ceil(area.name.length / 2);
          const lines =
            oneLineSize < 0.8 && area.name.length > 3
              ? [area.name.slice(0, half), area.name.slice(half)]
              : [area.name];
          const longest = Math.max(...lines.map((line) => line.length));
          const fontSize = Math.max(
            0.5,
            Math.min(1.2, (area.widthM * 0.9) / longest, (area.heightM * 0.7) / lines.length),
          );
          const firstLineOffset = ((lines.length - 1) / 2) * fontSize * 1.15;

          return (
            <g key={id}>
              <title>{`${area.name}（${area.widthM}m × ${area.heightM}m）`}</title>
              <rect
                x={x}
                y={y}
                width={area.widthM}
                height={area.heightM}
                className={`chart-area c${colorIndex(id)}`}
              />
              <text
                x={x + area.widthM / 2}
                y={y + area.heightM / 2 - firstLineOffset}
                fontSize={fontSize}
                className="chart-label"
                textAnchor="middle"
                dominantBaseline="central"
              >
                {lines.map((line, index) => (
                  <tspan
                    key={index}
                    x={x + area.widthM / 2}
                    dy={index === 0 ? 0 : fontSize * 1.15}
                  >
                    {line}
                  </tspan>
                ))}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption>{title}（単位：m）</figcaption>
    </figure>
  );
}
