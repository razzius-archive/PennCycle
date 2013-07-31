from base import *

import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_URL = 'https://s3.amazonaws.com/penncycle/'

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost')
}
