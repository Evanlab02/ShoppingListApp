echo "Creating missing migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Starting admin server..."
gunicorn -b 0.0.0.0:80 -w 1 --log-config shoppingapp/logging.config --capture-output --log-level info --worker-class uvicorn_worker.UvicornWorker 'shoppingapp.config.asgi:app'
