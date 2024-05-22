"""Contains the entry to the serverless azure function app."""

import azure.functions as func

from shoppingapp.config.asgi import main  # type: ignore

django_app = main()
app = func.AsgiFunctionApp(app=django_app, http_auth_level=func.AuthLevel.ANONYMOUS)
