#!/bin/sh
echo "Waiting for Postgres..."

# wait until Postgres container is ready to accept connections
while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - starting Django"
exec "$@"