FROM python:3.11.6-slim

COPY version.txt version.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /src

COPY /src/authentication /src/authentication
COPY /src/stores /src/stores
COPY /src/items /src/items
COPY /src/shoppingapp /src/shoppingapp

EXPOSE 80

CMD ["gunicorn","-b" ,"0.0.0.0:80", "-w" ,"4" ,"--worker-class" ,"uvicorn.workers.UvicornWorker", "'shoppingapp.config.asgi:main()'"]