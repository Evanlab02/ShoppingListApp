FROM python:3.10.0-slim-buster

RUN apt-get update \
    && apt-get install libpq-dev -y \
    && apt-get clean

COPY authenticationapp /app/authenticationapp
COPY shoppingapp /app/shoppingapp
COPY shoppingitem /app/shoppingitem
COPY shoppinglist /app/shoppinglist
COPY manage.py /app/manage.py
COPY application.properties /app/application.properties

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "shoppingapp.configs.asgi:application", "--host", "0.0.0.0"]