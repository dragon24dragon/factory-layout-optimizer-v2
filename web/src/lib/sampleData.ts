// サンプルデータ（ヒアリングで決めた工場の条件）を、計算で使う形に直す。
// 元データは ../data/sample_factory.json の写し。Python 版と同じものを使う。
import raw from "../data/sample_factory.json";
import type { Area, DailyFlow, Factory } from "./layout";

export const projectName: string = raw.project?.name ?? "工場レイアウト最適化";

export const factory: Factory = {
  widthM: raw.factory.width_m,
  heightM: raw.factory.height_m,
};

export const areas: Area[] = raw.areas.map((area) => ({
  id: area.id,
  name: area.name,
  count: area.count,
  widthM: area.width_m,
  heightM: area.height_m,
}));

export const dailyFlows: DailyFlow[] = raw.daily_flows;
