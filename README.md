# 工場設計レイアウト最適化ツール PoC
工場内の設備・エリア配置候補を生成し、搬送回数を考慮した移動距離スコアでランキングするPoCです。

Python / Streamlit / pytest / matplotlib を使用しています。

## 主な機能

- 工場内の設備・エリア配置候補を自動生成
- 搬送回数を考慮した移動距離スコアを計算
- 複数の配置候補をランキング表示
- StreamlitによるブラウザUI
- matplotlibによるレイアウト可視化
- pytestによる自動テスト

## 実行方法

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

Streamlitアプリを起動します。

```bash
streamlit run app.py
```

## テスト

pytestで自動テストを実行できます。

```bash
pytest
```

現在、37件のテストがすべて成功しています。

## プロジェクト構成

```text
factory-layout-optimizer-v2/
├─ app.py
├─ data/
│  └─ sample_factory.json
├─ layout_optimizer/
│  ├─ models.py
│  ├─ constraints.py
│  ├─ generator.py
│  ├─ scoring.py
│  └─ validation.py
├─ tests/
├─ requirements.txt
└─ README.md
```

## 現在のPoCについて

現段階では、グリッド配置と配置順の変更によって複数のレイアウト候補を生成し、
搬送距離スコアが小さい候補を上位にランキングします。

厳密な数理最適化ではなく、工場レイアウト最適化の考え方を検証するためのPoCです。