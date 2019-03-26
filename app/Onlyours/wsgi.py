"""
WSGI config for o project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if "DJANGO_SETTINGS_MODULE" not in os.environ:
    error_message = (
        'You have to put settings through "DJANGO_SETTINGS_MODULE" environment '
        'variable'
    )
    raise Exception(error_message)

application = get_wsgi_application()
