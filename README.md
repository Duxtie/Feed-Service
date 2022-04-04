## Installation

Make sure you have Docker and [Docker Compose](https://docs.docker.com/compose/install/) installed.

1. Ensure you are in the `the root directory` directory
2. Run `docker-compose up -d` (this will download and build the various images)
3. Visit `http://localhost:8001/docs` to access an automatic interactive documentation with Swagger UI (from the OpenAPI backend)
3. Visit `http://localhost:5050` to access PGAdmin, PostgreSQL web administration
3. Visit `http://localhost:5556` Flower, administration of Celery tasks
4. Use the `./assets/files/feed_upload_exmaple.xml` to run test upload

Use your browser to interact with the feed service using these URLs:

API, JSON based web API based on OpenAPI: http://localhost:8001/api/v1/feeds

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8001/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:8001/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050

Flower, administration of Celery tasks: http://localhost:5556