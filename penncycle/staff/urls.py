from django.conf.urls import patterns

from views import (
    Dashboard, checkout, checkin, PaymentsList,
    satisfy_payment, CreatePayment
)

urlpatterns = patterns(
    '',
    (r'^$', Dashboard.as_view()),
    (r'checkout/$', checkout),
    (r'checkin/$', checkin),
    (r'payments/$', PaymentsList.as_view()),
    (r'satisfy_payment/$', satisfy_payment),
    (r'create_payment/$', CreatePayment.as_view(success_url="/admin/create_payment")),
)
