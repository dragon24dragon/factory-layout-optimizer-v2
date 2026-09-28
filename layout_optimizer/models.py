from dataclasses import dataclass


@dataclass
class Factory:
    width_m: float
    height_m: float


@dataclass
class Area:
    id: str
    name: str
    count: int
    width_m: float
    height_m: float


@dataclass
class PlacedArea:
    area: Area
    x_m: float
    y_m: float