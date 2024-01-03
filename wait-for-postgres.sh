#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

# Extract the IP address of the "db" service
db_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' db)

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$db_ip" -p 5432 -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd