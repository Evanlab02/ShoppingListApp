FROM caddy:2.7.5-alpine

COPY --from=ghcr.io/evanlab02/shopping-web:latest /var/www/html/static/ /var/www/html/custom/static/
COPY --from=ghcr.io/evanlab02/shopping-web:latest /var/www/html/docs/ /var/www/html/custom/docs/
