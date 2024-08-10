FROM python:3.12.4-alpine3.20

RUN apk add --no-cache bash
COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY version.txt version.txt

WORKDIR /backend

COPY backend/authentication /backend/authentication
COPY backend/stores /backend/stores
COPY backend/items /backend/items
COPY backend/shoppingapp /backend/shoppingapp
COPY backend/dashboard /backend/dashboard

COPY backend/manage.py /backend/manage.py

CMD ["python","manage.py", "runserver"]
