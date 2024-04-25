FROM caddy:2.7.5-alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY static/ /var/www/html/static/
COPY htmlco[v]/ /var/www/html/htmlcov/

EXPOSE 80
