#!/bin/sh

echo "Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "Starting application with Gunicorn..."
exec gunicorn -b 0.0.0.0:5000 app:app