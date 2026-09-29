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
`postgres/initialize-database.sql` when PostgreSQL initializes a new data
directory. Existing PostgreSQL data volumes are not reinitialized.
