from django.conf.urls import patterns
from phonegap_views import check_for_student, signup, verify, send_pin

urlpatterns = patterns(
    '',
    (r'check_for_student/$', check_for_student),
    (r'signup/$', signup),
    (r'verify/$', verify),
    (r'send_pin/$', send_pin),
)
