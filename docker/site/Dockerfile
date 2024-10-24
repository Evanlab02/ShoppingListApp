FROM node:20.17.0-alpine3.20 AS build

COPY frontend/ /app/
WORKDIR /app
RUN npm ci
RUN npm run build

FROM caddy:2.7.5-alpine

COPY site/Caddyfile /etc/caddy/Caddyfile
COPY backend/static/ /var/www/html/static/
COPY --from=build /app/dist /var/www/html/site/

EXPOSE 80
EXPOSE 9999
