// 初めて見る人向けの使い方。操作の順番・数字の読み方・まだできないことだけを書く。

export default function Guide() {
  return (
    <section className="guide" aria-labelledby="guide-title">
      <h2 id="guide-title">使い方（3ステップ）</h2>
      <ol className="steps">
        <li>
          <strong>工場の条件を見る</strong>
          <span>
            「入力データ」に、工場の広さ（50m × 50m）と、置く設備（10種類・18台）が出ています。
            「1日あたりの搬送回数」を開くと、どこからどこへ1日に何回運ぶかが見られます。
          </span>
        </li>
        <li>
          <strong>条件を変える（変えなくても動きます）</strong>
          <span>
            「生成する候補数」は、作って比べる配置案の数です。
            「外壁からの距離」と「設備間の基本間隔」は、壁や隣の設備からどれだけ離すかです。
            間隔を広げすぎると工場に入りきらず、どの設備が置けなかったかを知らせます。
          </span>
        </li>
        <li>
          <strong>赤いボタンを押して、結果を見比べる</strong>
          <span>
            配置案を自動で作り、良い順に並べます。上位3案は配置図で見比べられます。
          </span>
        </li>
      </ol>

      <div className="guide-grid">
        <div className="guide-box">
          <h3>順位の決め方</h3>
          <p>
            設備と設備の距離に、1日に運ぶ回数をかけて合計します（搬送距離スコア）。
            <strong>小さいほど、毎日運ぶ距離が短い配置</strong>です。
            よく通る区間ほど点数への影響が大きくなるので、「よく通る道が短い配置」が上位に来ます。
          </p>
        </div>
        <div className="guide-box">
          <h3>この試作でまだできないこと</h3>
          <ul>
            <li>柱・非常口の前・電気室を避けて置くこと</li>
            <li>安全基準（通路幅、溶接エリアと置場の距離など）を満たさない案を外すこと</li>
            <li>配置案の作り方は「並べる順番を変える」だけなので、似た案が並びやすい</li>
          </ul>
        </div>
      </div>
    </section>
  );
}
