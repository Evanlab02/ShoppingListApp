FROM python:3.12.4-alpine3.20

RUN apk add --no-cache bash
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY version.txt version.txt

WORKDIR /src

COPY src/authentication /src/authentication
COPY src/stores /src/stores
COPY src/items /src/items
COPY src/shoppingapp /src/shoppingapp
COPY src/dashboard /src/dashboard

EXPOSE 80

CMD ["gunicorn","-b" ,"0.0.0.0:80", "-w" ,"4" ,"--worker-class" ,"uvicorn_worker.UvicornWorker", "'shoppingapp.config.asgi:main()'"]
