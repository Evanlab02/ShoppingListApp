python manage.py makemigrations
python manage.py migrate
gunicorn -b 0.0.0.0:80 -w 1 --log-config shoppingapp/logging.config --capture-output --log-level info --worker-class uvicorn_worker.UvicornWorker 'shoppingapp.config.asgi:app'
