"""Contains the entry to the serverless azure function app."""

import azure.functions as func

from shoppingapp.config.wsgi import application

app = func.WsgiFunctionApp(app=application, http_auth_level=func.AuthLevel.ANONYMOUS)
