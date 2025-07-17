#!/bin/sh

# This script is the entrypoint for the Docker container.
# It runs database migrations, creates initial data, and then starts the web server.

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create a superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py create_superuser_if_not_exists

# Create example jobs for demonstration
echo "Creating example jobs..."
python manage.py create_example_jobs

# Start the Gunicorn web server
echo "Starting Gunicorn server..."
exec gunicorn ResuMate_backend.wsgi:application --bind 0.0.0.0:$PORT
