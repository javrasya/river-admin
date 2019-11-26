__author__ = 'ahmetdal'

# !/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get("PRODUCTION", "false").lower() == "false":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
