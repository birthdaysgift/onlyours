from .base import *


ALLOWED_HOSTS.append("localhost")

DEBUG = True

DATABASES["default"] = {
    "ENGINE": 'django.db.backends.postgresql_psycopg2',
    "NAME": "onlyours_db",
    "USER": "postgres",
    "PASSWORD": "0000",
    "HOST": "localhost",
    "PORT": 5432
}
