import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db.session import SessionLocal
from app.models.vehicle import Bike, Car, Spaceship

DATA = Path(__file__).resolve().parents[1] / "data"

def load(filename):
    path = DATA / filename
    if not path.exists():
        print(f"  skipping {filename} not found")
        return []
    records = json.load(path.open())
    return [r for r in records if not all(isinstance(v, str) for v in r.values())]

def seed():
    db = SessionLocal()
    try:
        cars = load("cars.json")
        if cars:
            db.query(Car).delete()
            for r in cars:
                db.add(Car(
                    vehicle_type="car", model=r["model"], year=r["year"],
                    manufacturer=r["make"], colour=r.get("colour"),
                    engine_size=r.get("engine_size"), horsepower=r.get("horsepower"),
                    seats=r.get("seats"), top_speed=r.get("top_speed"),
                ))
            db.commit()
            print(f"  {len(cars)} cars")

        bikes = load("bikes.json")
        if bikes:
            db.query(Bike).delete()
            for r in bikes:
                db.add(Bike(
                    vehicle_type="bike", model=r["model"], year=r["year"],
                    manufacturer=r["brand"], gears=r.get("gears"),
                    type=r.get("type"), wheel_size=r.get("wheel_size"),
                ))
            db.commit()
            print(f"  {len(bikes)} bikes")

        spaceships = load("spaceships.json")
        if spaceships:
            db.query(Spaceship).delete()
            for r in spaceships:
                db.add(Spaceship(
                    vehicle_type="spaceship", model=r["model"], year=r["year"],
                    manufacturer=r["manufacturer"], max_crew=r.get("max_crew"),
                    top_speed=r.get("top_speed"),
                ))
            db.commit()
            print(f"  {len(spaceships)} spaceships")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding:")
    seed()
    print("Done")
