import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "工場レイアウト設計最適化ツール PoC",
  description:
    "設備の配置候補を自動で作り、「距離 × 1日の搬送回数」で順位をつけて上位3案を見比べられる試作です。",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
