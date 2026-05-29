import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from strawberry.fastapi import GraphQLRouter
from app.db.session import Base
from app.graphql.schema import schema
from app.models.vehicle import Bike, Car, Spaceship

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSession = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    from app.main import app
    async def ctx():
        yield {"db": db}
    app.router.routes = [r for r in app.router.routes if not getattr(r, "path", "").startswith("/graphql")]
    app.include_router(GraphQLRouter(schema, context_getter=ctx), prefix="/graphql")
    with TestClient(app) as c:
        yield c

@pytest.fixture
def data(db):
    db.add_all([
        Car(vehicle_type="car", model="EcoNova", year=2020, manufacturer="Astoria",
            colour="Blue", engine_size=4.8, horsepower=214, seats=5, top_speed=253.0),
        Bike(vehicle_type="bike", model="Urbanite", year=2014, manufacturer="EraCraft",
             gears=3, type="Road", wheel_size=29),
        Spaceship(vehicle_type="spaceship", model="Celestial Voyager", year=2004,
                  manufacturer="Pulsar Ventures", max_crew=50, top_speed=0.21),
    ])
    db.commit()

def gql(client, query, variables=None):
    res = client.post("/graphql", json={"query": query, **({"variables": variables} if variables else {})})
    assert res.status_code == 200
    body = res.json()
    assert "errors" not in body, body.get("errors")
    return body["data"]

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_list_cars(client, data):
    assert gql(client, "{ cars { total } }")["cars"]["total"] == 1

def test_list_bikes(client, data):
    assert gql(client, "{ bikes { total } }")["bikes"]["total"] == 1

def test_list_spaceships(client, data):
    assert gql(client, "{ spaceships { total } }")["spaceships"]["total"] == 1

def test_search_vehicles(client, data):
    res = gql(client, '{ searchVehicles(keyword: "Voyager") { __typename ... on SpaceshipType { model } } }')
    assert res["searchVehicles"][0]["__typename"] == "SpaceshipType"