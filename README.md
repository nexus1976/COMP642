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

### Part B
See `/mongo/mongo-init.js` for the creation of the database and collection. This is also where you'll find the datbase collection being seeded with flexible data representing metadata enrichment for events, specifically `Description`, `Speakers`, `Schedule`, `Reviews`, and `Tags`. This file meets the following requirements:
- `insertOne()` and `insertMany()`
- Indexing
- Arrays
- Nested documents

See the endpoint defined in `api/services/events_router.py` the `get_event_content` method to see the use of `find()`.
See the endpoint defined in `api/services/events_router.py` the `create_event_review` method to see the use of Updates.
See the endpoint defined in `api/services/events_router.py` the `delete_event_reviews` method to see the use of Deletes.

WIP: Still need to demonstrate 8 meaningful queries against MongoDB and cover:
- Projection
- Comparison operators
- Boolean operators
- Dot notation
- $elemMatch

Include these queries:
Find events containing a particular tag.
Find events featuring a particular speaker.
Find events with reviews above a specified rating.
Find events containing particular combinations of nested attributes.
Find concerts belonging to a particular genre.
