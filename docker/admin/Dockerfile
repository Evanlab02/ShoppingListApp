FROM python:3.11.6-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY version.txt src/version.txt

WORKDIR /src

COPY /src/authentication /src/authentication
COPY /src/stores /src/stores
COPY /src/items /src/items
COPY /src/shoppingapp /src/shoppingapp
COPY /src/manage.py /src/manage.py

CMD ["python","manage.py", "runserver"]