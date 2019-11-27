__author__ = 'ahmetdal'

# !/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get("PRODUCTION_DEMO", "false").lower() == "true":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.prod")
    elif os.environ.get("LOCAL_DEMO", "false").lower() == "true":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
