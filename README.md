**Vehicle Query Engine**

I have built this GraphQL API using FastAPI and PostgreSQL to browse, search, and filter vehicles like cars, bikes, and spaceships as per the requirements given.

**Why I built it this way**

The requirement was for a clean API to browse and search vehicles across different types without using any third party frameworks or tools for searching, filtering and other operations. I chose GraphQL over REST here for two reasons one it fits this use case better where instead of building separate endpoints for cars, bikes, and spaceships, one endpoint handles everything and another Xanadu preferred it to be the techstack. The client decides what fields it needs, which means no over fetching.

For the database I used joined table inheritance, a shared vehicles table holds the common fields like model, year, and manufacturer, and each vehicle type has its own table for type specific columns. With this approach, the schema stays clean and adding a new vehicle type later is easier by adding a new table. I used Alembic for migrations because schema changes need to be versioned, anyone cloning the repo gets the exact same schema.

**Stack**

- **FastAPI** — Web framework
- **PostgreSQL** — Database
- **Strawberry** — GraphQL library
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations

**Project structure**

I ensure we follow the 12 factor app principles while structuring this project where 

- Configuration is separated from code
- Application is self contained
- DB is treated as a resource that can be swapped easily

The app folder is separated by as

- Models
- Database session
- GraphQL schema
- Configuration each lives in their own module

As I worked on tight deadline, I kept it minimal. In a production codebase, we can have a services layer between resolvers and the ORM with business logic, a repositories module for DB queries, and the GraphQL resolvers for mapping inputs and outputs. That would make unit testing easier and clear separation of functions between the layers.

**Setup**

**Docker**

If you have Docker Desktop in your local running, you can easily run the app in below one command setting up the db, migrations, seeding script, and the API

```bash
docker compose up --build
```
Open **http://localhost:8000/graphql** in any browser to validate.

**Local setup**

If you do not have docker, please follow below commands, I have given the commands for windows as I used them. Please feel free to change commands if you are using ios or any other OS.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```
You need to install postgres local instance and have it running in a port

```bash
psql -U postgres -c "CREATE USER vqe_user WITH PASSWORD 'vqe_pass';"
psql -U postgres -c "CREATE DATABASE vqe_db OWNER vqe_user;"
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```
Open **http://localhost:8000/graphql** in any browser to validate.

**Seeding script**

Seeding script handles the field descriptor row that comes as the first element in each JSON file and skips it automatically. We can run it multiple times as it clears and reloads the data each time.

**API**

The GraphQL explorer is available at /graphql and FastAPI docs in /docs. We can write and test queries directly in the browser.

I have listed few queries below for trying it out.

**List and filter bikes**

```graphql
{
  bikes(
    filters: { type: "Road", gears: { min: 5 } }
  ) {
    total
    items {
      id
      model
      manufacturer
      type
      gears
      wheelSize
      year
    }
  }
}
```

**Search across all vehicle types**

```graphql
{
  searchVehicles(keyword: "nova") {
    __typename
    ... on CarType {
      model
      manufacturer
      year
    }
    ... on BikeType {
      model
      manufacturer
    }
    ... on SpaceshipType {
      model
      manufacturer
    }
  }
}
```
**Filtering**

Every list query accepts a filters argument. Text filters like manufacturer and model do a partial case-insensitive match so searching "ast" will match "Astoria". Range filters use { min, max } and both are optional so you can do just a min or just a max.

**Sorting**

Pass sort: { field: FIELD_NAME, direction: ASC } to any list query. We can do ascending or descending directions

**Pagination**

Default page size: 20
Max: 100.
Every response includes total, page, pageSize, and totalPages

**Health checks**

GET /health — returns 200 if the server is running

GET /status — returns 200 if the server can reach the database

**Search implementation**

Search is implemented using PostgreSQL's ILIKE operator. Filtering, sorting, and pagination all happen at the database level through SQLAlchemy queries without any external dependencies. For the small dataset size in this project this is more than sufficient. Database indexes can be added on frequently queried columns such as model, manufacturer, and bike type to improve query performance for large datasets.

**Tests**

The current tests covers only the main behaviors like listing, filtering, sorting, pagination, and cross type search as a sample. We can later expand to cover more scenarios like below:

- Empty strings, special characters in search terms, and boundary values on range filters
- Invalid input handling
- Each filter field checked individually
- Performance, load, regression, code vulnerability, coverage, and other tests

We have around 75% code coverage and can be expanded later to cover more scenarios as the project grows. To run the tests, run pytest in the project root.

**How we can better structure in a real production service**

- The GraphQL resolvers can be moved into a separate module
- DataLoader batching can be added to prevent potential N+1 query problems
- Authentication and authorization would be added as middleware with respective permissions handled at the GraphQL layer
- Asynchronous database sessions can be enabled using SQLAlchemy's async session
- Observability can be configured with logging, metrics, and tracing
- A CI/CD pipeline can be built to run linting, type checking, and integration and performance load tests

**Brainstorming**

While designing the database schema I noticed that the three vehicle types share some fields but each has columns that are unrelated to the others, a spaceship does not have seats, a bike does not have horsepower. I first considered a single flat table with nullable columns for everything, which is simpler to set up but produces a messy schema where half the columns are always NULL depending on the type. I later decided to go with joined table inheritance, a shared vehicles table for common fields and separate tables for each type. The tradeoff is that queries do a JOIN, but for this scale that is irrelevant and the schema clarity is worth it. While normalizing the manufacturer field I noticed that in the provided data cars use make, bikes use brand, and spaceships use manufacturer, three different keys for the same concept. The seed script handles this mapping so the database always stores it as manufacturer regardless of which JSON file it came from. Comments and docstrings have not been added but will be included in a production codebase. 

If you have any feedback or suggestions on this implementation, feel free to open an issue on the repository. I am open to discussions on alternative approaches, improvements, or anything that could make this better.

**Kaviyaa Vasudevan**
