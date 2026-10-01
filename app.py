import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
import streamlit as st

from layout_optimizer.generator import generate_ranked_layouts
from layout_optimizer.models import Area, Factory


def configure_japanese_font():
    preferred_fonts = [
        "Yu Gothic",
        "Meiryo",
        "MS Gothic",
    ]

    available_fonts = {
        font.name
        for font in fm.fontManager.ttflist
    }

    for font_name in preferred_fonts:
        if font_name in available_fonts:
            plt.rcParams["font.family"] = font_name
            plt.rcParams["axes.unicode_minus"] = False
            return


configure_japanese_font()


DATA_PATH = Path("data/sample_factory.json")


def load_sample_data() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_factory(data: dict) -> Factory:
    factory_data = data["factory"]

    return Factory(
        width_m=factory_data["width_m"],
        height_m=factory_data["height_m"],
    )


def build_areas(data: dict) -> list[Area]:
    return [
        Area(
            id=area["id"],
            name=area["name"],
            count=area["count"],
            width_m=area["width_m"],
            height_m=area["height_m"],
        )
        for area in data["areas"]
    ]


def draw_layout(
    factory: Factory,
    layout: dict,
    title: str,
):
    fig, ax = plt.subplots(figsize=(9, 7))

    ax.set_xlim(0, factory.width_m)
    ax.set_ylim(0, factory.height_m)
    ax.set_aspect("equal")

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(title)

    ax.grid(True, alpha=0.25)

    for placed_area in layout.values():
        area = placed_area.area

        rectangle = Rectangle(
            (placed_area.x_m, placed_area.y_m),
            area.width_m,
            area.height_m,
            fill=False,
            linewidth=2,
        )

        ax.add_patch(rectangle)

        center_x = placed_area.x_m + area.width_m / 2
        center_y = placed_area.y_m + area.height_m / 2

        # 名前が四角に収まるように、文字の大きさを決める。
        # もとの決め方（幅だけを見る）に加えて、名前の長さも見る。
        # 長い名前のときだけ小さくなり、大きくなることはない。
        base_size = 5.0 if area.width_m <= 5 else 8.0
        points_per_meter = 10.0
        usable_points = area.width_m * points_per_meter * 0.75
        font_size = min(base_size, usable_points / len(area.name))

        ax.text(
            center_x,
            center_y,
            area.name,
            ha="center",
            va="center",
            fontsize=max(3.5, font_size),
            clip_on=True,
        )

    return fig


st.set_page_config(
    page_title="工場レイアウト設計最適化ツール PoC",
    layout="wide",
)

st.title("工場レイアウト設計最適化ツール PoC")

st.write(
    "設備の配置候補を生成し、"
    "搬送回数を考慮した移動距離でランキングします。"
)

try:
    data = load_sample_data()
except Exception as error:
    st.error(f"サンプルデータを読み込めませんでした: {error}")
    st.stop()


project_name = data.get("project", {}).get(
    "name",
    "工場レイアウト最適化",
)

factory = build_factory(data)
areas = build_areas(data)
daily_flows = data.get("daily_flows", [])


st.subheader("入力データ")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "工場の幅",
        f"{factory.width_m} m",
    )

with col2:
    st.metric(
        "工場の奥行き",
        f"{factory.height_m} m",
    )

with col3:
    st.metric(
        "設備・エリア種類数",
        len(areas),
    )


with st.expander("設備・エリア一覧"):
    area_rows = []

    for area in areas:
        area_rows.append(
            {
                "ID": area.id,
                "名称": area.name,
                "台数": area.count,
                "幅(m)": area.width_m,
                "奥行き(m)": area.height_m,
            }
        )

    st.dataframe(
        area_rows,
        use_container_width=True,
    )


st.subheader("探索条件")

condition_col1, condition_col2, condition_col3 = st.columns(3)

with condition_col1:
    candidate_count = st.number_input(
        "生成する候補数",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
    )

with condition_col2:
    wall_clearance_m = st.number_input(
        "外壁からの距離 (m)",
        min_value=0.0,
        value=1.0,
        step=0.5,
    )

with condition_col3:
    gap_m = st.number_input(
        "設備間の基本間隔 (m)",
        min_value=0.0,
        value=2.0,
        step=0.5,
    )


st.caption(
    "※ 現段階のPoCでは、候補生成はグリッド配置と配置順の変更を使い、"
    "搬送距離スコアで比較します。"
)


if st.button(
    "レイアウト候補を生成・ランキング",
    type="primary",
):
    try:
        ranked = generate_ranked_layouts(
            factory=factory,
            areas=areas,
            daily_flows=daily_flows,
            candidate_count=int(candidate_count),
            wall_clearance_m=float(wall_clearance_m),
            gap_m=float(gap_m),
        )

    except ValueError as error:
        st.error(str(error))
        st.stop()

    except Exception as error:
        st.error(
            f"レイアウト生成中にエラーが発生しました: {error}"
        )
        st.stop()


    if not ranked:
        st.warning("レイアウト候補を生成できませんでした。")
        st.stop()


    st.success(
        f"{len(ranked)}件の候補を生成し、ランキングしました。"
    )

    st.subheader("ランキング")

    ranking_rows = []

    for rank, candidate in enumerate(ranked, start=1):
        ranking_rows.append(
            {
                "順位": rank,
                "候補ID": candidate["candidate_id"],
                "搬送距離スコア": round(
                    candidate["score"],
                    2,
                ),
            }
        )

    st.dataframe(
        ranking_rows,
        use_container_width=True,
        hide_index=True,
    )


    display_count = min(3, len(ranked))

    st.subheader(
        f"上位{display_count}案"
    )

    for rank, candidate in enumerate(
        ranked[:display_count],
        start=1,
    ):
        st.markdown(
            f"### 第{rank}位"
        )

        st.write(
            f"候補ID: {candidate['candidate_id']}"
        )

        st.write(
            "搬送距離スコア: "
            f"{candidate['score']:.2f}"
        )

        fig = draw_layout(
            factory=factory,
            layout=candidate["layout"],
            title=(
                f"Rank {rank} "
                f"- Score {candidate['score']:.2f}"
            ),
        )

        st.pyplot(fig)

        plt.close(fig)


st.divider()

st.caption(
    f"{project_name} / "
    "Factory Layout Optimizer PoC"
)