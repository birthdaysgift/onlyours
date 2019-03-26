#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    settings_from_args = None
    for arg in sys.argv:
        if '--settings=' in arg:
            settings_from_args = arg.split('=')[1]
    if settings_from_args is None:
        error_message = (
            'You have to put settings by --settings option. '
            'Example: python manage.py runserver --settings=path.to.settings'
        )
        raise Exception(error_message)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_from_args)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
