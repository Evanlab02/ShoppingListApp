FROM caddy:2.7.5-alpine

COPY src/Caddyfile /etc/caddy/Caddyfile
COPY src/static/ /var/www/html/static/
COPY src/htmlco[v]/ /var/www/html/htmlcov/

EXPOSE 80
EXPOSE 9999
