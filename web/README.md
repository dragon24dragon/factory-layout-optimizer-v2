# web — Vercel 公開用（Next.js 版）

工場レイアウト設計最適化ツール PoC（v2）を、ブラウザだけで動く形にしたもの。
計算は `../layout_optimizer/`（Python 版）を `src/lib/layout.ts` に移したもので、
**同じ入力なら同じ順位・スコア・配置になる**ことをテストで確かめている。

```bash
npm install
npm run dev     # http://localhost:3000
npm test        # Python 版との突き合わせ（src/lib/__fixtures__/python_results.json）
npm run build   # Vercel と同じ本番ビルド
```

- データ：`src/data/sample_factory.json`（`../data/sample_factory.json` の写し。直したら両方そろえる）
- Python 版の計算を変えたら、正解表 `python_results.json` を作り直してから `npm test` を通す
- Vercel では **Root Directory を `web`** にする
