FROM python:3.11.6-slim

RUN apt-get update \
    && apt-get install make -y \
    && apt-get clean

RUN pip install pipenv

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY shoppingapp /app/shoppingapp
COPY manage.py /app/manage.py

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "shoppingapp.configs.asgi:application", "--host", "0.0.0.0"]