#!/bin/bash
# entrypoint.sh

# Wait for PostgreSQL to be ready
./wait-for-postgres.sh db:5432

# Run Django migrations and start the application

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
