"use client";

import { useState } from "react";
import LayoutChart from "./LayoutChart";
import { generateRankedLayouts, type RankedCandidate } from "@/lib/layout";
import { areas, dailyFlows, factory } from "@/lib/sampleData";

type Result =
  | { kind: "ok"; ranked: RankedCandidate[] }
  | { kind: "error"; message: string };

function NumberField({
  label,
  value,
  onChange,
  min,
  max,
  step,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max?: number;
  step: number;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      <input
        type="number"
        inputMode="decimal"
        value={Number.isNaN(value) ? "" : value}
        min={min}
        max={max}
        step={step}
        onChange={(event) => onChange(event.target.valueAsNumber)}
      />
    </label>
  );
}

export default function Optimizer() {
  const [candidateCount, setCandidateCount] = useState(5);
  const [wallClearanceM, setWallClearanceM] = useState(1.0);
  const [gapM, setGapM] = useState(2.0);
  const [result, setResult] = useState<Result | null>(null);

  const totalUnits = areas.reduce((sum, area) => sum + area.count, 0);

  function run() {
    if (
      !Number.isInteger(candidateCount) ||
      candidateCount < 1 ||
      candidateCount > 20
    ) {
      setResult({ kind: "error", message: "生成する候補数は1〜20の整数で入力してください。" });
      return;
    }
    if (Number.isNaN(wallClearanceM) || wallClearanceM < 0) {
      setResult({ kind: "error", message: "外壁からの距離は0以上で入力してください。" });
      return;
    }
    if (Number.isNaN(gapM) || gapM < 0) {
      setResult({ kind: "error", message: "設備間の基本間隔は0以上で入力してください。" });
      return;
    }

    try {
      const ranked = generateRankedLayouts(
        factory,
        areas,
        dailyFlows,
        candidateCount,
        wallClearanceM,
        gapM,
      );

      if (ranked.length === 0) {
        setResult({ kind: "error", message: "レイアウト候補を生成できませんでした。" });
        return;
      }

      setResult({ kind: "ok", ranked });
    } catch (error) {
      setResult({
        kind: "error",
        message: error instanceof Error ? error.message : String(error),
      });
    }
  }

  return (
    <>
      <section>
        <h2>入力データ</h2>
        <div className="metrics">
          <div className="metric">
            <span>工場の幅</span>
            <strong>{factory.widthM} m</strong>
          </div>
          <div className="metric">
            <span>工場の奥行き</span>
            <strong>{factory.heightM} m</strong>
          </div>
          <div className="metric">
            <span>設備・エリア</span>
            <strong>
              {areas.length}種類・{totalUnits}台
            </strong>
          </div>
        </div>

        <details className="panel">
          <summary>設備・エリア一覧</summary>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>名称</th>
                  <th className="num">台数</th>
                  <th className="num">幅 (m)</th>
                  <th className="num">奥行き (m)</th>
                </tr>
              </thead>
              <tbody>
                {areas.map((area) => (
                  <tr key={area.id}>
                    <td>{area.name}</td>
                    <td className="num">{area.count}</td>
                    <td className="num">{area.widthM}</td>
                    <td className="num">{area.heightM}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>

        <details className="panel">
          <summary>1日あたりの搬送回数</summary>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>どこから</th>
                  <th>どこへ</th>
                  <th className="num">回/日</th>
                </tr>
              </thead>
              <tbody>
                {dailyFlows.map((flow) => (
                  <tr key={`${flow.from}-${flow.to}`}>
                    <td>{nameOf(flow.from)}</td>
                    <td>{nameOf(flow.to)}</td>
                    <td className="num">{flow.trips_per_day}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      </section>

      <section>
        <h2>探索条件</h2>
        <div className="fields">
          <NumberField
            label="生成する候補数"
            value={candidateCount}
            onChange={setCandidateCount}
            min={1}
            max={20}
            step={1}
          />
          <NumberField
            label="外壁からの距離 (m)"
            value={wallClearanceM}
            onChange={setWallClearanceM}
            min={0}
            step={0.5}
          />
          <NumberField
            label="設備間の基本間隔 (m)"
            value={gapM}
            onChange={setGapM}
            min={0}
            step={0.5}
          />
        </div>
        <p className="caption">
          ※ 現段階のPoCでは、候補生成はグリッド配置と配置順の変更を使い、搬送距離スコアで比較します。
        </p>
        <button type="button" className="primary" onClick={run}>
          レイアウト候補を生成・ランキング
        </button>
      </section>

      {result?.kind === "error" && (
        <p className="notice error" role="alert">
          {result.message}
        </p>
      )}

      {result?.kind === "ok" && (
        <section>
          <p className="notice ok" role="status">
            {result.ranked.length}件の候補を生成し、ランキングしました。
          </p>

          <h2>ランキング</h2>
          <p className="caption">
            搬送距離スコア ＝ 設備間の距離 × 1日の搬送回数 の合計。小さいほど、運ぶ距離が短い配置です。
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th className="num">順位</th>
                  <th className="num">候補ID</th>
                  <th className="num">搬送距離スコア</th>
                </tr>
              </thead>
              <tbody>
                {result.ranked.map((candidate, index) => (
                  <tr key={candidate.candidateId}>
                    <td className="num">{index + 1}</td>
                    <td className="num">{candidate.candidateId}</td>
                    <td className="num">{candidate.score.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h2>上位{Math.min(3, result.ranked.length)}案</h2>
          <div className="charts">
            {result.ranked.slice(0, 3).map((candidate, index) => (
              <article key={candidate.candidateId} className="card">
                <h3>第{index + 1}位</h3>
                <p className="card-meta">
                  候補ID：{candidate.candidateId}　／　搬送距離スコア：{candidate.score.toFixed(2)}
                </p>
                <LayoutChart
                  factory={factory}
                  layout={candidate.layout}
                  title={`第${index + 1}位の配置図`}
                />
              </article>
            ))}
          </div>
        </section>
      )}
    </>
  );
}

function nameOf(flowId: string): string {
  return flowId
    .split("_or_")
    .map((part) => areas.find((area) => area.id === part)?.name ?? part)
    .join(" または ");
}
