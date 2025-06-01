FROM python:3.13.2-alpine3.21 AS docs-builder

ENV UV_SYSTEM_PYTHON 1

RUN apk add --no-cache bash
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY docs/requirements.txt requirements.txt
RUN uv pip install -r requirements.txt

COPY docs/mkdocs.yml /content/mkdocs.yml
COPY docs/docs/ /content/docs/

WORKDIR /content

RUN mkdocs build

FROM caddy:2.7.5-alpine

COPY web/Caddyfile /etc/caddy/Caddyfile
COPY backend/static/ /var/www/html/static/
COPY --from=docs-builder /content/site/ /var/www/html/docs/

EXPOSE 80
