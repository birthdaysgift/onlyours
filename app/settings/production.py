from .common import *

# Use environment variables to keep secret key in production
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS.append("onlyours.herokuapp.com")

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "d72vqj3j6b7mi0",
        "USER": "tesbefqtelaofw",
        "PASSWORD": "b61ee5ebbdebebfec2c8b0571d8ea1a9d25a0d25ab91fb2a906c63c2e6dd8d7d",
        "HOST": "ec2-54-163-234-99.compute-1.amazonaws.com",
        "PORT": "5432"
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 1
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
