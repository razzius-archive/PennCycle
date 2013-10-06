from django.conf.urls import patterns

from views import (
    Index, BikeDashboard, checkout, checkin
)

urlpatterns = patterns(
    '',
    (r'^$', Index.as_view()),
    # url(r'^checkouts/$', BikeDashboard.as_view(), name="bike dashboard"),
    (r'checkout/$', checkout),
    (r'checkin/$', checkin),
)
