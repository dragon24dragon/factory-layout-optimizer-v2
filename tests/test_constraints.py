from layout_optimizer.constraints import (
    areas_overlap,
    distance_between_areas,
    has_minimum_distance,
    has_pillar_clearance,
    has_wall_clearance,
    has_welding_clearance,
    is_clear_of_emergency_exit,
    is_inside_factory,
)
from layout_optimizer.models import Area, Factory, PlacedArea


def test_area_inside_factory_returns_true():
    factory = Factory(50, 50)
    area = Area("cutting_machine", "切断機", 1, 4, 3)
    placed_area = PlacedArea(area, 10, 20)

    assert is_inside_factory(factory, placed_area) is True


def test_area_outside_factory_returns_false():
    factory = Factory(50, 50)
    area = Area("cutting_machine", "切断機", 1, 4, 3)
    placed_area = PlacedArea(area, 48, 49)

    assert is_inside_factory(factory, placed_area) is False


def test_overlapping_areas_return_true():
    first_area = Area("machine_a", "設備A", 1, 4, 3)
    second_area = Area("machine_b", "設備B", 1, 4, 3)

    first = PlacedArea(first_area, 10, 10)
    second = PlacedArea(second_area, 12, 11)

    assert areas_overlap(first, second) is True


def test_separated_areas_return_false():
    first_area = Area("machine_a", "設備A", 1, 4, 3)
    second_area = Area("machine_b", "設備B", 1, 4, 3)

    first = PlacedArea(first_area, 10, 10)
    second = PlacedArea(second_area, 20, 20)

    assert areas_overlap(first, second) is False


def test_distance_between_areas_is_two_meters():
    first_area = Area("machine_a", "設備A", 1, 4, 3)
    second_area = Area("machine_b", "設備B", 1, 4, 3)

    first = PlacedArea(first_area, 10, 10)
    second = PlacedArea(second_area, 16, 10)

    assert distance_between_areas(first, second) == 2.0


def test_minimum_distance_two_meters_returns_true():
    first_area = Area("machine_a", "設備A", 1, 4, 3)
    second_area = Area("machine_b", "設備B", 1, 4, 3)

    first = PlacedArea(first_area, 10, 10)
    second = PlacedArea(second_area, 16, 10)

    assert has_minimum_distance(first, second, 2.0) is True


def test_less_than_minimum_distance_returns_false():
    first_area = Area("machine_a", "設備A", 1, 4, 3)
    second_area = Area("machine_b", "設備B", 1, 4, 3)

    first = PlacedArea(first_area, 10, 10)
    second = PlacedArea(second_area, 15.5, 10)

    assert has_minimum_distance(first, second, 2.0) is False


def test_wall_clearance_one_meter_returns_true():
    factory = Factory(50, 50)
    area = Area("machine_a", "設備A", 1, 4, 3)
    placed_area = PlacedArea(area, 1, 1)

    assert has_wall_clearance(factory, placed_area, 1.0) is True


def test_less_than_wall_clearance_returns_false():
    factory = Factory(50, 50)
    area = Area("machine_a", "設備A", 1, 4, 3)
    placed_area = PlacedArea(area, 0.5, 1)

    assert has_wall_clearance(factory, placed_area, 1.0) is False


def test_pillar_clearance_one_meter_returns_true():
    machine_area = Area("machine_a", "設備A", 1, 4, 3)
    pillar_area = Area("pillar", "柱", 1, 0.6, 0.6)

    machine = PlacedArea(machine_area, 10, 10)
    pillar = PlacedArea(pillar_area, 15, 10)

    assert has_pillar_clearance(machine, pillar, 1.0) is True


def test_less_than_pillar_clearance_returns_false():
    machine_area = Area("machine_a", "設備A", 1, 4, 3)
    pillar_area = Area("pillar", "柱", 1, 0.6, 0.6)

    machine = PlacedArea(machine_area, 10, 10)
    pillar = PlacedArea(pillar_area, 14.5, 10)

    assert has_pillar_clearance(machine, pillar, 1.0) is False


def test_area_clear_of_emergency_exit_returns_true():
    machine_area = Area("machine_a", "設備A", 1, 4, 3)
    clearance_area = Area(
        "emergency_exit_clearance",
        "非常口前安全範囲",
        1,
        3,
        3,
    )

    machine = PlacedArea(machine_area, 10, 10)
    clearance = PlacedArea(clearance_area, 20, 20)

    assert is_clear_of_emergency_exit(machine, clearance) is True


def test_area_overlapping_emergency_exit_returns_false():
    machine_area = Area("machine_a", "設備A", 1, 4, 3)
    clearance_area = Area(
        "emergency_exit_clearance",
        "非常口前安全範囲",
        1,
        3,
        3,
    )

    machine = PlacedArea(machine_area, 21, 21)
    clearance = PlacedArea(clearance_area, 20, 20)

    assert is_clear_of_emergency_exit(machine, clearance) is False


def test_welding_to_raw_material_five_meters_returns_true():
    welding_area = Area("welding_area", "溶接エリア", 1, 6, 5)
    raw_material_area = Area(
        "raw_material_storage",
        "原材料置場",
        1,
        15,
        10,
    )

    welding = PlacedArea(welding_area, 10, 10)
    raw_material = PlacedArea(raw_material_area, 21, 10)

    assert has_welding_clearance(welding, raw_material) is True


def test_welding_to_raw_material_less_than_five_meters_returns_false():
    welding_area = Area("welding_area", "溶接エリア", 1, 6, 5)
    raw_material_area = Area(
        "raw_material_storage",
        "原材料置場",
        1,
        15,
        10,
    )

    welding = PlacedArea(welding_area, 10, 10)
    raw_material = PlacedArea(raw_material_area, 20.5, 10)

    assert has_welding_clearance(welding, raw_material) is False


def test_welding_to_finished_goods_five_meters_returns_true():
    welding_area = Area("welding_area", "溶接エリア", 1, 6, 5)
    finished_goods_area = Area(
        "finished_goods_storage",
        "完成品置場",
        1,
        15,
        10,
    )

    welding = PlacedArea(welding_area, 10, 10)
    finished_goods = PlacedArea(finished_goods_area, 21, 10)

    assert has_welding_clearance(welding, finished_goods) is True


def test_welding_to_finished_goods_less_than_five_meters_returns_false():
    welding_area = Area("welding_area", "溶接エリア", 1, 6, 5)
    finished_goods_area = Area(
        "finished_goods_storage",
        "完成品置場",
        1,
        15,
        10,
    )

    welding = PlacedArea(welding_area, 10, 10)
    finished_goods = PlacedArea(finished_goods_area, 20.5, 10)

    assert has_welding_clearance(welding, finished_goods) is False