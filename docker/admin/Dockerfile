FROM python:3.11.6-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY version.txt src/version.txt

WORKDIR /src

COPY authentication /src/authentication
COPY stores /src/stores
COPY items /src/items
COPY shoppingapp /src/shoppingapp
COPY manage.py /src/manage.py

CMD ["python","manage.py", "runserver"]
