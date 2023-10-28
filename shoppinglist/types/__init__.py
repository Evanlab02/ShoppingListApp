"""Contains types used by the shopping list app."""

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
)
from django.http import HttpRequest
from ninja import Router, Schema

__all__ = [
    "User",
    "Model",
    "CharField",
    "IntegerField",
    "ForeignKey",
    "ManyToManyField",
    "DateField",
    "DateTimeField",
    "DecimalField",
    "TextField",
    "CASCADE",
    "Schema",
    "HttpRequest",
    "Router",
]
