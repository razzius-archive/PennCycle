from django.conf.urls.defaults import *
from app.views import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', index),
)
