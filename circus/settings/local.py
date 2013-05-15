from base import *

DEBUG = True

INTERNAL_IPS = ('127.0.0.1', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djraty-user',
        'USER': 'djraty-user',
        'PASSWORD': 'm4|<E1-5*',
        'HOST': 'localhost',
    }
}

SECRET_KEY = '-c3uh&e$0bl80udwokq*-acnam+d$$ioh9l_h0+9f2-!r&=&@a'
