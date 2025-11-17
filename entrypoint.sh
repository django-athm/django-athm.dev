#!/bin/sh
set -e

# Run migrations only if AUTO_MIGRATE is set to "True"
if [ "$AUTO_MIGRATE" = "True" ]; then
  echo "Running migrations..."
  uv run python manage.py migrate --noinput
else
  echo "Skipping auto-migrations (AUTO_MIGRATE=$AUTO_MIGRATE)"
  echo "To run migrations manually: docker-compose exec web uv run python manage.py migrate"
fi

# Execute the main command
exec "$@"
