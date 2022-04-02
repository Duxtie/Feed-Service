#! /usr/bin/env bash

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py


#celery worker -A app.worker -l info -Q main-queue -c 1

#celery -A app.worker worker -l info -Q main-queue -c 1