#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import execute_from_command_line


def main():
    """Run administrative tasks."""
    DEFAULT_SETTINGS = "shoppingapp.settings.settings"
    SETTINGS_MODULE = os.getenv("DEFAULT_SETTINGS_MODULE", DEFAULT_SETTINGS)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
