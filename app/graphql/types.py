from typing import Annotated, Union
import strawberry

@strawberry.type
class CarType:
    id: int
    model: str
    year: int
    manufacturer: str
    colour: str | None
    engine_size: float | None
    horsepower: int | None
    seats: int | None
    top_speed: float | None

@strawberry.type
class BikeType:
    id: int
    model: str
    year: int
    manufacturer: str
    gears: int | None
    type: str | None
    wheel_size: int | None

@strawberry.type
class SpaceshipType:
    id: int
    model: str
    year: int
    manufacturer: str
    max_crew: int | None
    top_speed: float | None

VehicleUnion = Annotated[
    Union[CarType, BikeType, SpaceshipType],
    strawberry.union("VehicleUnion"),
]

@strawberry.type
class PaginatedCars:
    items: list[CarType]
    total: int
    page: int
    page_size: int
    total_pages: int

@strawberry.type
class PaginatedBikes:
    items: list[BikeType]
    total: int
    page: int
    page_size: int
    total_pages: int

@strawberry.type
class PaginatedSpaceships:
    items: list[SpaceshipType]
    total: int
    page: int
    page_size: int
    total_pages: int
