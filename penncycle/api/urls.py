from django.conf.urls import patterns, url
from django.conf import settings

from api.views import Signup, check_for_student

urlpatterns = patterns(
    '',
    url('check$', check_for_student),
    url('signup$', Signup.as_view()),
)
