from layout_optimizer.models import Area, PlacedArea
from layout_optimizer.scoring import (
    center_distance,
    center_of_area,
    rank_candidate_layouts,
    total_weighted_flow_distance,
    weighted_flow_distance,
)


def test_center_of_area():
    area = Area("machine_a", "設備A", 1, 4, 6)
    placed_area = PlacedArea(area, 10, 20)

    assert center_of_area(placed_area) == (12.0, 23.0)


def test_center_distance_is_five_meters():
    first_area = Area("machine_a", "設備A", 1, 4, 4)
    second_area = Area("machine_b", "設備B", 1, 4, 4)

    first = PlacedArea(first_area, 0, 0)
    second = PlacedArea(second_area, 3, 4)

    assert center_distance(first, second) == 5.0


def test_weighted_flow_distance():
    first_area = Area("machine_a", "設備A", 1, 4, 4)
    second_area = Area("machine_b", "設備B", 1, 4, 4)

    first = PlacedArea(first_area, 0, 0)
    second = PlacedArea(second_area, 3, 4)

    assert weighted_flow_distance(first, second, 10) == 50.0


def test_total_weighted_flow_distance():
    area_a = Area("machine_a", "設備A", 1, 4, 4)
    area_b = Area("machine_b", "設備B", 1, 4, 4)
    area_c = Area("machine_c", "設備C", 1, 4, 4)

    placed_areas = {
        "machine_a": PlacedArea(area_a, 0, 0),
        "machine_b": PlacedArea(area_b, 3, 4),
        "machine_c": PlacedArea(area_c, 6, 8),
    }

    daily_flows = [
        {
            "from": "machine_a",
            "to": "machine_b",
            "trips_per_day": 10,
        },
        {
            "from": "machine_b",
            "to": "machine_c",
            "trips_per_day": 20,
        },
    ]

    assert total_weighted_flow_distance(placed_areas, daily_flows) == 150.0


def test_unknown_area_in_flow_is_ignored():
    area_a = Area("machine_a", "設備A", 1, 4, 4)
    area_b = Area("machine_b", "設備B", 1, 4, 4)

    placed_areas = {
        "machine_a": PlacedArea(area_a, 0, 0),
        "machine_b": PlacedArea(area_b, 3, 4),
    }

    daily_flows = [
        {
            "from": "machine_a",
            "to": "machine_b",
            "trips_per_day": 10,
        },
        {
            "from": "unknown_machine",
            "to": "machine_b",
            "trips_per_day": 100,
        },
    ]

    assert total_weighted_flow_distance(placed_areas, daily_flows) == 50.0


def test_rank_candidate_layouts_sorts_by_lowest_score():
    area_a = Area("machine_a", "設備A", 1, 4, 4)
    area_b = Area("machine_b", "設備B", 1, 4, 4)

    layouts = [
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 10, 0),
        },
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 3, 4),
        },
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 1, 0),
        },
    ]

    daily_flows = [
        {
            "from": "machine_a",
            "to": "machine_b",
            "trips_per_day": 10,
        },
    ]

    ranked = rank_candidate_layouts(
        layouts,
        daily_flows,
    )

    assert [candidate["score"] for candidate in ranked] == [
        10.0,
        50.0,
        100.0,
    ]


def test_rank_candidate_layouts_keeps_original_candidate_id():
    area_a = Area("machine_a", "設備A", 1, 4, 4)
    area_b = Area("machine_b", "設備B", 1, 4, 4)

    layouts = [
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 10, 0),
        },
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 3, 4),
        },
        {
            "machine_a": PlacedArea(area_a, 0, 0),
            "machine_b": PlacedArea(area_b, 1, 0),
        },
    ]

    daily_flows = [
        {
            "from": "machine_a",
            "to": "machine_b",
            "trips_per_day": 10,
        },
    ]

    ranked = rank_candidate_layouts(
        layouts,
        daily_flows,
    )

    assert [candidate["candidate_id"] for candidate in ranked] == [
        3,
        2,
        1,
    ]

def test_flow_to_multiple_units_is_split_evenly():
    source = Area("source", "置場", 1, 2, 2)
    machine_1 = Area("machine_1", "設備1", 1, 2, 2)
    machine_2 = Area("machine_2", "設備2", 1, 2, 2)

    placed_areas = {
        "source": PlacedArea(source, 0, 0),
        "machine_1": PlacedArea(machine_1, 3, 4),
        "machine_2": PlacedArea(machine_2, 6, 8),
    }

    daily_flows = [
        {"from": "source", "to": "machine", "trips_per_day": 30},
    ]

    # 30回を2台に15回ずつ：5m × 15回 ＋ 10m × 15回
    assert total_weighted_flow_distance(placed_areas, daily_flows) == 225.0


def test_or_group_includes_units_of_both_areas():
    source = Area("source", "置場", 1, 2, 2)
    lathe = Area("lathe", "旋盤", 1, 2, 2)
    mill_1 = Area("mill_1", "フライス1", 1, 2, 2)

    placed_areas = {
        "source": PlacedArea(source, 0, 0),
        "lathe": PlacedArea(lathe, 3, 4),
        "mill_1": PlacedArea(mill_1, 6, 8),
    }

    daily_flows = [
        {"from": "source", "to": "mill_or_lathe", "trips_per_day": 10},
    ]

    # 10回を旋盤とフライスの2台に5回ずつ：10m × 5回 ＋ 5m × 5回
    assert total_weighted_flow_distance(placed_areas, daily_flows) == 75.0


def test_similar_id_is_not_mixed_in():
    source = Area("source", "置場", 1, 2, 2)
    machine_1 = Area("machine_1", "設備1", 1, 2, 2)
    machine_big_1 = Area("machine_big_1", "大型設備1", 1, 2, 2)

    placed_areas = {
        "source": PlacedArea(source, 0, 0),
        "machine_1": PlacedArea(machine_1, 3, 4),
        "machine_big_1": PlacedArea(machine_big_1, 30, 40),
    }

    daily_flows = [
        {"from": "source", "to": "machine", "trips_per_day": 10},
    ]

    assert total_weighted_flow_distance(placed_areas, daily_flows) == 50.0


def test_every_flow_in_sample_data_is_counted():
    import json
    from pathlib import Path

    from layout_optimizer.generator import generate_grid_layout
    from layout_optimizer.models import Factory
    from layout_optimizer.scoring import resolve_units

    data = json.loads(
        Path("data/sample_factory.json").read_text(encoding="utf-8")
    )
    factory = Factory(
        data["factory"]["width_m"],
        data["factory"]["height_m"],
    )
    areas = [
        Area(a["id"], a["name"], a["count"], a["width_m"], a["height_m"])
        for a in data["areas"]
    ]
    layout = generate_grid_layout(factory, areas)

    for flow in data["daily_flows"]:
        assert resolve_units(flow["from"], layout), flow["from"]
        assert resolve_units(flow["to"], layout), flow["to"]
