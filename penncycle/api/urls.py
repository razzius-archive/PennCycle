from django.conf.urls import patterns, url
from django.conf import settings

from api.views import Signup

urlpatterns = patterns(
    '',
    url('signup$', Signup.as_view()),
) 
