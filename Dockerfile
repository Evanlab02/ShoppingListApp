FROM python:3.11.6-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY manage.py /app/manage.py
COPY pyproject.toml /app/pyproject.toml
COPY version.txt /app/version.txt
COPY authentication /app/authentication
COPY stores /app/stores
COPY items /app/items
COPY shoppingapp /app/shoppingapp

EXPOSE 80

CMD ["gunicorn","-b" ,"0.0.0.0:80", "-w" ,"8" ,"--worker-class" ,"uvicorn.workers.UvicornWorker", "'shoppingapp.config.asgi:main()'"]