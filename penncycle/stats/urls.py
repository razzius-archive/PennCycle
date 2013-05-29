from django.conf.urls import patterns
from views import *

urlpatterns = patterns(
    '',
    (r'signups/$', signups),
    (r'schools/$', schools),
    (r'majors/$', majors),
    (r'numrides/$', numrides),
    (r'emails/$', emails),
    (r'current_emails/$', current_emails),
    (r'duration/$', duration),
    (r'gender/$', gender),
    (r'housing/$', housing),
    (r'paid/$', paid),
    (r'year/$', year),
    (r'payment/$', payment),
    (r'waived/$', waived),
    (r'checkouts/$', checkouts),
    (r'dump/$', dump),
)
