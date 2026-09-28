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
    trips_per_day: int,
) -> float:
    distance_m = center_distance(first, second)

    return distance_m * trips_per_day


def total_weighted_flow_distance(
    placed_areas: dict[str, PlacedArea],
    daily_flows: list[dict],
) -> float:
    total = 0.0

    for flow in daily_flows:
        from_id = flow["from"]
        to_id = flow["to"]
        trips_per_day = flow["trips_per_day"]

        if from_id not in placed_areas:
            continue

        if to_id not in placed_areas:
            continue

        total += weighted_flow_distance(
            placed_areas[from_id],
            placed_areas[to_id],
            trips_per_day,
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