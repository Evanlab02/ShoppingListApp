FROM caddy:2.7.5-alpine

COPY site/Caddyfile /etc/caddy/Caddyfile
COPY backend/static/ /var/www/html/static/

EXPOSE 80
EXPOSE 9999
