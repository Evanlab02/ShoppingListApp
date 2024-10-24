FROM python:3.12.4-alpine3.20 AS docs

RUN apk add --no-cache bash
COPY docs/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /documentation

COPY docs/ /documentation
RUN mkdocs build

FROM node:20.17.0-alpine3.20 AS build

COPY frontend/ /app/
WORKDIR /app
RUN npm ci
RUN npm run build

FROM caddy:2.7.5-alpine

COPY site/Caddyfile /etc/caddy/Caddyfile
COPY backend/static/ /var/www/html/static/
COPY --from=build /app/dist /var/www/html/site/
COPY --from=docs /documentation/site /var/www/html/docs/

EXPOSE 80
EXPOSE 9999
