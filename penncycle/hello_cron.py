import os
from os.path import abspath, dirname
import sys
path = '~/penncycle'
if path not in sys.path:
    sys.path.append(path)
sys.path.insert(0, path)
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from app.models import *
from app.views import email_alex

message = 'hello'
email_alex('hello!')