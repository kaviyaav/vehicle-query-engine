from enum import Enum
import strawberry

@strawberry.enum
class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

@strawberry.input
class IntRangeInput:
    min: int | None = None
    max: int | None = None

@strawberry.input
class FloatRangeInput:
    min: float | None = None
    max: float | None = None

@strawberry.input
class CarFilterInput:
    manufacturer: str | None = None
    model: str | None = None
    colour: str | None = None
    year: IntRangeInput | None = None
    horsepower: IntRangeInput | None = None
    engine_size: FloatRangeInput | None = None
    seats: IntRangeInput | None = None
    top_speed: FloatRangeInput | None = None

@strawberry.enum
class CarSortField(Enum):
    YEAR = "year"
    HORSEPOWER = "horsepower"
    ENGINE_SIZE = "engine_size"
    TOP_SPEED = "top_speed"
    MANUFACTURER = "manufacturer"

@strawberry.input
class CarSortInput:
    field: CarSortField = CarSortField.YEAR
    direction: SortDirection = SortDirection.ASC

@strawberry.input
class BikeFilterInput:
    manufacturer: str | None = None
    model: str | None = None
    type: str | None = None
    year: IntRangeInput | None = None
    gears: IntRangeInput | None = None
    wheel_size: IntRangeInput | None = None

@strawberry.enum
class BikeSortField(Enum):
    YEAR = "year"
    GEARS = "gears"
    WHEEL_SIZE = "wheel_size"
    MANUFACTURER = "manufacturer"

@strawberry.input
class BikeSortInput:
    field: BikeSortField = BikeSortField.YEAR
    direction: SortDirection = SortDirection.ASC

@strawberry.input
class SpaceshipFilterInput:
    manufacturer: str | None = None
    model: str | None = None
    year: IntRangeInput | None = None
    max_crew: IntRangeInput | None = None
    top_speed: FloatRangeInput | None = None

@strawberry.enum
class SpaceshipSortField(Enum):
    YEAR = "year"
    MAX_CREW = "max_crew"
    TOP_SPEED = "top_speed"
    MANUFACTURER = "manufacturer"

@strawberry.input
class SpaceshipSortInput:
    field: SpaceshipSortField = SpaceshipSortField.YEAR
    direction: SortDirection = SortDirection.ASC
