import math
import strawberry
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from app.graphql.inputs import (
    BikeFilterInput, BikeSortInput, CarFilterInput, CarSortInput, SpaceshipFilterInput, 
    SpaceshipSortInput, SortDirection,
)
from app.graphql.types import (
    BikeType, CarType, SpaceshipType, VehicleUnion, PaginatedBikes, PaginatedCars, PaginatedSpaceships,
)
from app.models.vehicle import Bike, Car, Spaceship

def _ordering(direction: SortDirection):
    return asc if direction.value == "asc" else desc

def _paging(total: int, page: int, page_size: int) -> dict:
    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(page, total_pages))
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "offset": (page - 1) * page_size,
    }

def _cars(db: Session, filters, sort, page, page_size) -> PaginatedCars:
    q = select(Car)

    if filters:
        if filters.manufacturer:
            q = q.where(Car.manufacturer.ilike(f"%{filters.manufacturer}%"))
        if filters.model:
            q = q.where(Car.model.ilike(f"%{filters.model}%"))
        if filters.colour:
            q = q.where(Car.colour.ilike(filters.colour))
        if filters.year:
            if filters.year.min is not None:
                q = q.where(Car.year >= filters.year.min)
            if filters.year.max is not None:
                q = q.where(Car.year <= filters.year.max)
        if filters.horsepower:
            if filters.horsepower.min is not None:
                q = q.where(Car.horsepower >= filters.horsepower.min)
            if filters.horsepower.max is not None:
                q = q.where(Car.horsepower <= filters.horsepower.max)
        if filters.engine_size:
            if filters.engine_size.min is not None:
                q = q.where(Car.engine_size >= filters.engine_size.min)
            if filters.engine_size.max is not None:
                q = q.where(Car.engine_size <= filters.engine_size.max)
        if filters.seats:
            if filters.seats.min is not None:
                q = q.where(Car.seats >= filters.seats.min)
            if filters.seats.max is not None:
                q = q.where(Car.seats <= filters.seats.max)
        if filters.top_speed:
            if filters.top_speed.min is not None:
                q = q.where(Car.top_speed >= filters.top_speed.min)
            if filters.top_speed.max is not None:
                q = q.where(Car.top_speed <= filters.top_speed.max)

    sort_col = getattr(Car, sort.field.value if sort else "year")
    sort_dir = _ordering(sort.direction if sort else SortDirection.ASC)
    q = q.order_by(sort_dir(sort_col))

    meta = _paging(db.scalar(select(func.count()).select_from(q.subquery())), page, page_size)
    rows = db.scalars(q.offset(meta["offset"]).limit(page_size)).all()

    return PaginatedCars(
        items=[
            CarType(
                id=r.id, model=r.model, year=r.year, manufacturer=r.manufacturer,
                colour=r.colour, engine_size=r.engine_size, horsepower=r.horsepower,
                seats=r.seats, top_speed=r.top_speed,
            )
            for r in rows
        ],
        **{k: v for k, v in meta.items() if k != "offset"},
    )

def _bikes(db: Session, filters, sort, page, page_size) -> PaginatedBikes:
    q = select(Bike)

    if filters:
        if filters.manufacturer:
            q = q.where(Bike.manufacturer.ilike(f"%{filters.manufacturer}%"))
        if filters.model:
            q = q.where(Bike.model.ilike(f"%{filters.model}%"))
        if filters.type:
            q = q.where(Bike.type.ilike(filters.type))
        if filters.year:
            if filters.year.min is not None:
                q = q.where(Bike.year >= filters.year.min)
            if filters.year.max is not None:
                q = q.where(Bike.year <= filters.year.max)
        if filters.gears:
            if filters.gears.min is not None:
                q = q.where(Bike.gears >= filters.gears.min)
            if filters.gears.max is not None:
                q = q.where(Bike.gears <= filters.gears.max)
        if filters.wheel_size:
            if filters.wheel_size.min is not None:
                q = q.where(Bike.wheel_size >= filters.wheel_size.min)
            if filters.wheel_size.max is not None:
                q = q.where(Bike.wheel_size <= filters.wheel_size.max)

    sort_col = getattr(Bike, sort.field.value if sort else "year")
    sort_dir = _ordering(sort.direction if sort else SortDirection.ASC)
    q = q.order_by(sort_dir(sort_col))

    meta = _paging(db.scalar(select(func.count()).select_from(q.subquery())), page, page_size)
    rows = db.scalars(q.offset(meta["offset"]).limit(page_size)).all()

    return PaginatedBikes(
        items=[
            BikeType(
                id=r.id, model=r.model, year=r.year, manufacturer=r.manufacturer,
                gears=r.gears, type=r.type, wheel_size=r.wheel_size,
            )
            for r in rows
        ],
        **{k: v for k, v in meta.items() if k != "offset"},
    )

def _spaceships(db: Session, filters, sort, page, page_size) -> PaginatedSpaceships:
    q = select(Spaceship)

    if filters:
        if filters.manufacturer:
            q = q.where(Spaceship.manufacturer.ilike(f"%{filters.manufacturer}%"))
        if filters.model:
            q = q.where(Spaceship.model.ilike(f"%{filters.model}%"))
        if filters.year:
            if filters.year.min is not None:
                q = q.where(Spaceship.year >= filters.year.min)
            if filters.year.max is not None:
                q = q.where(Spaceship.year <= filters.year.max)
        if filters.max_crew:
            if filters.max_crew.min is not None:
                q = q.where(Spaceship.max_crew >= filters.max_crew.min)
            if filters.max_crew.max is not None:
                q = q.where(Spaceship.max_crew <= filters.max_crew.max)
        if filters.top_speed:
            if filters.top_speed.min is not None:
                q = q.where(Spaceship.top_speed >= filters.top_speed.min)
            if filters.top_speed.max is not None:
                q = q.where(Spaceship.top_speed <= filters.top_speed.max)

    sort_col = getattr(Spaceship, sort.field.value if sort else "year")
    sort_dir = _ordering(sort.direction if sort else SortDirection.ASC)
    q = q.order_by(sort_dir(sort_col))

    meta = _paging(db.scalar(select(func.count()).select_from(q.subquery())), page, page_size)
    rows = db.scalars(q.offset(meta["offset"]).limit(page_size)).all()

    return PaginatedSpaceships(
        items=[
            SpaceshipType(
                id=r.id, model=r.model, year=r.year, manufacturer=r.manufacturer,
                max_crew=r.max_crew, top_speed=r.top_speed,
            )
            for r in rows
        ],
        **{k: v for k, v in meta.items() if k != "offset"},
    )

@strawberry.type
class Query:

    @strawberry.field
    def cars(
        self, info: Info,
        filters: CarFilterInput | None = None,
        sort: CarSortInput | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedCars:
        return _cars(info.context["db"], filters, sort, page, min(page_size, 100))

    @strawberry.field
    def bikes(
        self, info: Info,
        filters: BikeFilterInput | None = None,
        sort: BikeSortInput | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedBikes:
        return _bikes(info.context["db"], filters, sort, page, min(page_size, 100))

    @strawberry.field
    def spaceships(
        self, info: Info,
        filters: SpaceshipFilterInput | None = None,
        sort: SpaceshipSortInput | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedSpaceships:
        return _spaceships(info.context["db"], filters, sort, page, min(page_size, 100))

    @strawberry.field(description="Search across all vehicle types by model or manufacturer.")
    def search_vehicles(self, info: Info, keyword: str) -> list[VehicleUnion]:  
        db = info.context["db"]
        results: list = []

        for Model, TypeClass, extras in [
            (Car,       CarType,       ["colour", "engine_size", "horsepower", "seats", "top_speed"]),
            (Bike,      BikeType,      ["gears", "type", "wheel_size"]),
            (Spaceship, SpaceshipType, ["max_crew", "top_speed"]),
        ]:
            rows = db.scalars(
                select(Model).where(
                    Model.model.ilike(f"%{keyword}%") | Model.manufacturer.ilike(f"%{keyword}%")
                )
            ).all()
            for r in rows:
                kwargs = {"id": r.id, "model": r.model, "year": r.year, "manufacturer": r.manufacturer}
                for f in extras:
                    kwargs[f] = getattr(r, f, None)
                results.append(TypeClass(**kwargs))

        return results

schema = strawberry.Schema(query=Query)

def get_graphql_router(context_getter) -> GraphQLRouter:
    return GraphQLRouter(schema, context_getter=context_getter)
