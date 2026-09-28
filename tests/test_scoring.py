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