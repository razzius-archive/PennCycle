from django.conf.urls import patterns

from views import Dashboard, checkout, checkin, end_session

urlpatterns = patterns(
    '',
    (r'^$', Dashboard.as_view()),
    (r'checkout$', checkout),
    (r'checkin$', checkin),
    (r'logout$', end_session),
)
