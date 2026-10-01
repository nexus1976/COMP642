# COMP642 - Group Project
### Team
- Jean Paul Collazo
- Janeth Lucero Garcia Rodriguez
- Daniel Graham

## Application
All dependent components are composable locally with Docker. Simply run the following command at the root of this repo:
`docker compose up -d`

## Components
- Mongo
- Postgres
- Redis
- API (Backend Python FastAPI)
- Web app (Frontend Angular)

The Postgres image creates the tables defined by the SQLAlchemy models in
`api/infrastructure/postgres` and loads synthetic sample records from
`postgres/init.sql` when PostgreSQL initializes a new data
directory. Existing PostgreSQL data volumes are not reinitialized.

## Project Deliverables
### Part A
- See `postgres/init.sql` for the tables and 8 required queries. This file is what is used by Docker to create the database and tables and seed the data. The queries are commented out at the end for reference.
- See the endpoint defined in `api/services/orders_router.py` the `create_order` method that serves the `POST /orders` endpoint which demonstrates the transaction / rollback requirement.

