from .models import Area, Factory, PlacedArea
from .scoring import rank_candidate_layouts


def expand_areas(areas: list[Area]) -> list[Area]:
    expanded = []

    for area in areas:
        for index in range(area.count):
            if area.count == 1:
                area_id = area.id
                area_name = area.name
            else:
                area_id = f"{area.id}_{index + 1}"
                area_name = f"{area.name}{index + 1}"

            expanded.append(
                Area(
                    id=area_id,
                    name=area_name,
                    count=1,
                    width_m=area.width_m,
                    height_m=area.height_m,
                )
            )

    return expanded


def generate_grid_layout(
    factory: Factory,
    areas: list[Area],
    wall_clearance_m: float = 1.0,
    gap_m: float = 2.0,
) -> dict[str, PlacedArea]:
    expanded_areas = expand_areas(areas)

    placed_areas = {}

    current_x = wall_clearance_m
    current_y = wall_clearance_m
    row_height = 0.0

    usable_right = factory.width_m - wall_clearance_m
    usable_top = factory.height_m - wall_clearance_m

    for area in expanded_areas:
        if current_x + area.width_m > usable_right:
            current_x = wall_clearance_m
            current_y += row_height + gap_m
            row_height = 0.0

        if current_y + area.height_m > usable_top:
            raise ValueError(
                f"{area.name}を配置できません。工場内のスペースが不足しています。"
            )

        placed_areas[area.id] = PlacedArea(
            area=area,
            x_m=current_x,
            y_m=current_y,
        )

        current_x += area.width_m + gap_m
        row_height = max(row_height, area.height_m)

    return placed_areas


def generate_candidate_layouts(
    factory: Factory,
    areas: list[Area],
    candidate_count: int = 5,
    wall_clearance_m: float = 1.0,
    gap_m: float = 2.0,
) -> list[dict[str, PlacedArea]]:
    if candidate_count <= 0:
        return []

    expanded_areas = expand_areas(areas)

    if not expanded_areas:
        return []

    layouts = []
    number_of_variations = min(
        candidate_count,
        len(expanded_areas),
    )

    for shift in range(number_of_variations):
        reordered_areas = (
            expanded_areas[shift:]
            + expanded_areas[:shift]
        )

        layout = generate_grid_layout(
            factory=factory,
            areas=reordered_areas,
            wall_clearance_m=wall_clearance_m,
            gap_m=gap_m,
        )

        layouts.append(layout)

    return layouts


def generate_ranked_layouts(
    factory: Factory,
    areas: list[Area],
    daily_flows: list[dict],
    candidate_count: int = 5,
    wall_clearance_m: float = 1.0,
    gap_m: float = 2.0,
) -> list[dict]:
    layouts = generate_candidate_layouts(
        factory=factory,
        areas=areas,
        candidate_count=candidate_count,
        wall_clearance_m=wall_clearance_m,
        gap_m=gap_m,
    )

    ranked = rank_candidate_layouts(
        layouts,
        daily_flows,
    )

    return ranked