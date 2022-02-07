from core.config.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "menuvotedb",
        'USER': "devadmin",
        'PASSWORD': "Ninja6708",
        'HOST': "db",
        'PORT': "5432",
    }
}