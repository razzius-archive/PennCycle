from django.conf.urls import patterns

from views import (
    Dashboard, checkout, checkin
)

urlpatterns = patterns(
    '',
    (r'^$', Dashboard.as_view()),
    (r'checkout/$', checkout),
    (r'checkin/$', checkin),
)
