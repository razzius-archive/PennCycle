from django.conf.urls import patterns
from phonegap_views import (
    check_for_student, signup, verify, send_pin, bike_data,
    station_data, feedback, checkout, checkin
)

urlpatterns = patterns(
    '',
    (r'check_for_student/$', check_for_student),
    (r'signup/$', signup),
    (r'verify/$', verify),
    (r'send_pin/$', send_pin),

    (r'bike_data/$', bike_data),
    (r'station_data/$', station_data),
    (r'feedback/$', feedback),
    (r'checkout$', checkout),
    (r'checkin/$', checkin)
)
