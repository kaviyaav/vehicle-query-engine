from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    __mapper_args__ = {
        "polymorphic_on": "vehicle_type",
        "polymorphic_identity": "vehicle",
    }

class Car(Vehicle):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True)
    colour: Mapped[str | None] = mapped_column(String(60))
    engine_size: Mapped[float | None] = mapped_column(Float)
    horsepower: Mapped[int | None] = mapped_column(Integer)
    seats: Mapped[int | None] = mapped_column(Integer)
    top_speed: Mapped[float | None] = mapped_column(Float)
    __mapper_args__ = {"polymorphic_identity": "car"}

class Bike(Vehicle):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True)
    gears: Mapped[int | None] = mapped_column(Integer)
    type: Mapped[str | None] = mapped_column(String(60), index=True)
    wheel_size: Mapped[int | None] = mapped_column(Integer)
    __mapper_args__ = {"polymorphic_identity": "bike"}

class Spaceship(Vehicle):
    __tablename__ = "spaceships"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True)
    max_crew: Mapped[int | None] = mapped_column(Integer)
    top_speed: Mapped[float | None] = mapped_column(Float)
    __mapper_args__ = {"polymorphic_identity": "spaceship"}
