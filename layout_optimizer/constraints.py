from math import hypot

from .models import Factory, PlacedArea


def is_inside_factory(factory: Factory, placed_area: PlacedArea) -> bool:
    left = placed_area.x_m
    bottom = placed_area.y_m
    right = left + placed_area.area.width_m
    top = bottom + placed_area.area.height_m

    return (
        left >= 0
        and bottom >= 0
        and right <= factory.width_m
        and top <= factory.height_m
    )


def areas_overlap(first: PlacedArea, second: PlacedArea) -> bool:
    first_left = first.x_m
    first_right = first.x_m + first.area.width_m
    first_bottom = first.y_m
    first_top = first.y_m + first.area.height_m

    second_left = second.x_m
    second_right = second.x_m + second.area.width_m
    second_bottom = second.y_m
    second_top = second.y_m + second.area.height_m

    separated = (
        first_right <= second_left
        or second_right <= first_left
        or first_top <= second_bottom
        or second_top <= first_bottom
    )

    return not separated


def distance_between_areas(first: PlacedArea, second: PlacedArea) -> float:
    first_left = first.x_m
    first_right = first.x_m + first.area.width_m
    first_bottom = first.y_m
    first_top = first.y_m + first.area.height_m

    second_left = second.x_m
    second_right = second.x_m + second.area.width_m
    second_bottom = second.y_m
    second_top = second.y_m + second.area.height_m

    horizontal_gap = max(
        second_left - first_right,
        first_left - second_right,
        0,
    )

    vertical_gap = max(
        second_bottom - first_top,
        first_bottom - second_top,
        0,
    )

    return hypot(horizontal_gap, vertical_gap)


def has_minimum_distance(
    first: PlacedArea,
    second: PlacedArea,
    minimum_distance_m: float,
) -> bool:
    return distance_between_areas(first, second) >= minimum_distance_m


def has_wall_clearance(
    factory: Factory,
    placed_area: PlacedArea,
    minimum_distance_m: float,
) -> bool:
    left = placed_area.x_m
    bottom = placed_area.y_m
    right = placed_area.x_m + placed_area.area.width_m
    top = placed_area.y_m + placed_area.area.height_m

    return (
        left >= minimum_distance_m
        and bottom >= minimum_distance_m
        and factory.width_m - right >= minimum_distance_m
        and factory.height_m - top >= minimum_distance_m
    )


def has_pillar_clearance(
    placed_area: PlacedArea,
    pillar: PlacedArea,
    minimum_distance_m: float,
) -> bool:
    return distance_between_areas(placed_area, pillar) >= minimum_distance_m


def is_clear_of_emergency_exit(
    placed_area: PlacedArea,
    emergency_exit_clearance: PlacedArea,
) -> bool:
    return not areas_overlap(placed_area, emergency_exit_clearance)


def has_welding_clearance(
    welding_area: PlacedArea,
    other_area: PlacedArea,
    minimum_distance_m: float = 5.0,
) -> bool:
    return distance_between_areas(welding_area, other_area) >= minimum_distance_m