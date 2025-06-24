# Creating your custom web image

## Overview

Shopping List App runs behind a reverse proxy. We use **Caddy** as the proxy of choice in the reference deployment. The repository therefore contains a **very minimal Caddy image** that serves the static assets and documentation needed by the web tier.

While this image works out-of-the-box, many users already operate Caddy elsewhere or require additional routing, TLS, or authentication directives.

Below is a minimal example that shows how to build **your own** Caddy image while still bundling the static assets published by the official image.

```Dockerfile
FROM caddy:2.7.5-alpine

# Copy the reference implementation shipped at ghcr.io/evanlab02/shopping-web:latest
COPY --from=ghcr.io/evanlab02/shopping-web:latest /var/www/html/static/ /var/www/html/custom/static/
COPY --from=ghcr.io/evanlab02/shopping-web:latest /var/www/html/docs/   /var/www/html/custom/docs/
```

1. `caddy:2.7.5-alpine` is the **final (and only) runtime layer**.
2. Both the static files and the MkDocs documentation are copied from the official `shopping-web` image into `/var/www/html/custom/*`.

That’s it—setup is as straightforward as that. Mount (or rebuild) with your own `Caddyfile` whenever you need to tweak the proxy while still benefiting from the pre-packaged static assets.

> **Note**
> At this stage Shopping List App cannot easily be placed behind a path such as `/shopping/`. We highly recommend using a **sub-domain** to isolate the application from others. Path-based deployments will be supported in a future release.
