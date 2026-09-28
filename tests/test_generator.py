import pytest

from layout_optimizer.generator import (
    expand_areas,
    generate_candidate_layouts,
    generate_grid_layout,
    generate_ranked_layouts,
)
from layout_optimizer.models import Area, Factory


def test_expand_areas_with_multiple_count():
    areas = [
        Area("cutting_machine", "切断機", 2, 4, 3),
    ]

    expanded = expand_areas(areas)

    assert len(expanded) == 2
    assert expanded[0].id == "cutting_machine_1"
    assert expanded[0].name == "切断機1"
    assert expanded[1].id == "cutting_machine_2"
    assert expanded[1].name == "切断機2"


def test_generate_grid_layout_places_areas_from_lower_left():
    factory = Factory(50, 50)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
        Area("machine_b", "設備B", 1, 4, 3),
    ]

    layout = generate_grid_layout(
        factory,
        areas,
        wall_clearance_m=1.0,
        gap_m=2.0,
    )

    assert layout["machine_a"].x_m == 1.0
    assert layout["machine_a"].y_m == 1.0

    assert layout["machine_b"].x_m == 7.0
    assert layout["machine_b"].y_m == 1.0


def test_generate_grid_layout_moves_to_next_row():
    factory = Factory(12, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
        Area("machine_b", "設備B", 1, 4, 3),
        Area("machine_c", "設備C", 1, 4, 3),
    ]

    layout = generate_grid_layout(
        factory,
        areas,
        wall_clearance_m=1.0,
        gap_m=2.0,
    )

    assert layout["machine_a"].x_m == 1.0
    assert layout["machine_a"].y_m == 1.0

    assert layout["machine_b"].x_m == 7.0
    assert layout["machine_b"].y_m == 1.0

    assert layout["machine_c"].x_m == 1.0
    assert layout["machine_c"].y_m == 6.0


def test_generate_grid_layout_raises_error_when_space_is_insufficient():
    factory = Factory(10, 8)

    areas = [
        Area("machine", "設備", 2, 6, 3),
    ]

    with pytest.raises(
        ValueError,
        match="工場内のスペースが不足しています",
    ):
        generate_grid_layout(
            factory,
            areas,
            wall_clearance_m=1.0,
            gap_m=2.0,
        )


def test_generate_candidate_layouts_creates_five_candidates():
    factory = Factory(40, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
        Area("machine_b", "設備B", 1, 4, 3),
        Area("machine_c", "設備C", 1, 4, 3),
        Area("machine_d", "設備D", 1, 4, 3),
        Area("machine_e", "設備E", 1, 4, 3),
    ]

    layouts = generate_candidate_layouts(
        factory,
        areas,
        candidate_count=5,
        wall_clearance_m=1.0,
        gap_m=2.0,
    )

    assert len(layouts) == 5


def test_generate_candidate_layouts_changes_first_area():
    factory = Factory(40, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
        Area("machine_b", "設備B", 1, 4, 3),
        Area("machine_c", "設備C", 1, 4, 3),
        Area("machine_d", "設備D", 1, 4, 3),
        Area("machine_e", "設備E", 1, 4, 3),
    ]

    layouts = generate_candidate_layouts(
        factory,
        areas,
        candidate_count=5,
    )

    first_area_ids = [
        next(iter(layout))
        for layout in layouts
    ]

    assert first_area_ids == [
        "machine_a",
        "machine_b",
        "machine_c",
        "machine_d",
        "machine_e",
    ]


def test_generate_candidate_layouts_zero_count_returns_empty_list():
    factory = Factory(40, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
    ]

    layouts = generate_candidate_layouts(
        factory,
        areas,
        candidate_count=0,
    )

    assert layouts == []


def test_generate_ranked_layouts_returns_score_order():
    factory = Factory(40, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
        Area("machine_b", "設備B", 1, 4, 3),
        Area("machine_c", "設備C", 1, 4, 3),
    ]

    daily_flows = [
        {
            "from": "machine_a",
            "to": "machine_b",
            "trips_per_day": 20,
        },
        {
            "from": "machine_b",
            "to": "machine_c",
            "trips_per_day": 10,
        },
    ]

    ranked = generate_ranked_layouts(
        factory=factory,
        areas=areas,
        daily_flows=daily_flows,
        candidate_count=3,
        wall_clearance_m=1.0,
        gap_m=2.0,
    )

    assert [candidate["score"] for candidate in ranked] == [
        180.0,
        240.0,
        300.0,
    ]

    assert [candidate["candidate_id"] for candidate in ranked] == [
        1,
        3,
        2,
    ]


def test_generate_ranked_layouts_zero_count_returns_empty_list():
    factory = Factory(40, 20)

    areas = [
        Area("machine_a", "設備A", 1, 4, 3),
    ]

    ranked = generate_ranked_layouts(
        factory=factory,
        areas=areas,
        daily_flows=[],
        candidate_count=0,
    )

    assert ranked == []