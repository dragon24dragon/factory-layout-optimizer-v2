from math import hypot

from .models import PlacedArea


def center_of_area(placed_area: PlacedArea) -> tuple[float, float]:
    center_x = placed_area.x_m + placed_area.area.width_m / 2
    center_y = placed_area.y_m + placed_area.area.height_m / 2

    return center_x, center_y


def center_distance(first: PlacedArea, second: PlacedArea) -> float:
    first_x, first_y = center_of_area(first)
    second_x, second_y = center_of_area(second)

    return hypot(second_x - first_x, second_y - first_y)


def weighted_flow_distance(
    first: PlacedArea,
    second: PlacedArea,
    trips_per_day: float,
) -> float:
    distance_m = center_distance(first, second)

    return distance_m * trips_per_day


def resolve_units(
    flow_id: str,
    placed_areas: dict[str, PlacedArea],
) -> list[PlacedArea]:
    # 搬送回数の表は「台数で分ける前の名前」で書かれている。
    # 例：cutting_machine → cutting_machine_1 と cutting_machine_2
    # 「A_or_B」は「AかB」の意味で、両方の台をまとめて返す。
    if flow_id in placed_areas:
        return [placed_areas[flow_id]]

    units = []

    for part in flow_id.split("_or_"):
        if part in placed_areas:
            units.append(placed_areas[part])
            continue

        prefix = part + "_"

        for area_id, placed_area in placed_areas.items():
            suffix = area_id[len(prefix):]

            if area_id.startswith(prefix) and suffix.isdigit():
                units.append(placed_area)

    return units


def total_weighted_flow_distance(
    placed_areas: dict[str, PlacedArea],
    daily_flows: list[dict],
) -> float:
    total = 0.0

    for flow in daily_flows:
        from_units = resolve_units(flow["from"], placed_areas)
        to_units = resolve_units(flow["to"], placed_areas)
        trips_per_day = flow["trips_per_day"]

        if not from_units or not to_units:
            continue

        # 台が複数あるときは、回数をすべての組み合わせに均等に割り振る。
        # 例：原材料置場（1台）→ 切断機（2台）の30回は、15回ずつ。
        pair_count = len(from_units) * len(to_units)

        for from_unit in from_units:
            for to_unit in to_units:
                total += weighted_flow_distance(
                    from_unit,
                    to_unit,
                    trips_per_day / pair_count,
                )

    return total


def rank_candidate_layouts(
    layouts: list[dict[str, PlacedArea]],
    daily_flows: list[dict],
) -> list[dict]:
    ranked = []

    for candidate_id, layout in enumerate(layouts, start=1):
        score = total_weighted_flow_distance(
            layout,
            daily_flows,
        )

        ranked.append(
            {
                "candidate_id": candidate_id,
                "score": score,
                "layout": layout,
            }
        )

    ranked.sort(
        key=lambda candidate: candidate["score"]
    )

    return ranked