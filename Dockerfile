FROM python:3.10.0-slim-buster

RUN apt-get update \
    && apt-get install libpq-dev -y \
    && apt-get install make -y \
    && apt-get clean

RUN pip install pipenv

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY shoppingapp /app/shoppingapp
COPY authenticationapp /app/authenticationapp
COPY shoppingitem /app/shoppingitem
COPY shoppinglist /app/shoppinglist
COPY manage.py /app/manage.py

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "shoppingapp.configs.asgi:application", "--host", "0.0.0.0"]