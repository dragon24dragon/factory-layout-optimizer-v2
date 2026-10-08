import Guide from "@/components/Guide";
import Optimizer from "@/components/Optimizer";
import { projectName } from "@/lib/sampleData";

export default function Home() {
  return (
    <main className="page">
      <header className="hero">
        <p className="eyebrow">PoC（試作）</p>
        <h1>工場レイアウト設計最適化ツール</h1>
        <p>設備の配置候補を生成し、搬送回数を考慮した移動距離でランキングします。</p>
        <p className="caption">
          ※ 入力データは、ChatGPT に発注者役を依頼した模擬ヒアリングで決めた架空の工場の条件です。実在の企業・実案件ではありません。
        </p>
      </header>

      <Guide />

      <Optimizer />

      <footer className="footer">
        {projectName} ／ Factory Layout Optimizer PoC ／ © 2026 dragon24dragon
      </footer>
    </main>
  );
}
