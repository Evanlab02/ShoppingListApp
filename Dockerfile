FROM caddy:2.7.5-alpine

COPY app/Caddyfile /etc/caddy/Caddyfile
COPY dist /var/www/html/site/
COPY static /var/www/html/static/

EXPOSE 80

