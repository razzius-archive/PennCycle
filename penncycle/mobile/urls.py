from django.conf.urls import patterns
from phonegap_views import check_for_student, mobile_signup, verify

urlpatterns = patterns(
    '',
    (r'check_for_student/$', check_for_student),
    (r'signup/$', mobile_signup),
    (r'verify/$', verify),
)
