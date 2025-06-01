FROM python:3.13.2-alpine3.21

ENV UV_SYSTEM_PYTHON 1
ENV DJANGO_SETTINGS_MODULE shoppingapp.admin.settings

RUN apk add --no-cache bash
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY backend/requirements.txt requirements.txt
RUN uv pip install -r requirements.txt

COPY version.txt version.txt

WORKDIR /backend

COPY backend/shoppingapp/ /backend/shoppingapp/
COPY backend/shoppingapp/config /backend/shoppingapp/config
COPY backend/shoppingapp/schemas /backend/shoppingapp/schemas
COPY backend/shoppingapp/utilities /backend/shoppingapp/utilities
COPY backend/shoppingapp/__init__.py /backend/shoppingapp/__init__.py
COPY backend/shoppingapp/logging.config /backend/shoppingapp/logging.config

COPY backend/authentication /backend/authentication
COPY backend/stores /backend/stores
COPY backend/items /backend/items
COPY backend/dashboard /backend/dashboard

COPY backend/manage.py /backend/manage.py
COPY backend/static /backend/static
COPY scripts/admin.start.sh /backend/admin.start.sh

RUN chmod +x /backend/admin.start.sh

CMD ["sh", "./admin.start.sh"]
