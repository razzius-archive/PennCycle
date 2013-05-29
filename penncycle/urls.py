from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login
admin.autodiscover()

from app.views import *
from mobile.views import sms, debug

urlpatterns = patterns(
    '',
    url(r'^manage/', include(admin.site.urls)),
    url(r'^admin/', include('staff.urls')),
    url(r'^pc-admin/', include('staff.urls')),
    url(r'^login/$', login),

    # Normal pages
    (r'^$', index),
    (r'^signup/$', signup),
    (r'^faq/$', faq),
    (r'^safety/$', safety),
    (r'^team/$', team),
    (r'^partners/$', partners),
    (r'^locations/$', locations),
    (r'^plans/$', plans),
    (r'^thankyou/(\d{1,8})/$', thankyou),
    (r'^pay/(?P<payment_type>\w+)/(?P<penncard>\d{8})/(?P<plan>\d+)/$', pay),

    # Backend-related
    (r'^info_submit/$', info_submit),
    (r'^verify_payment/$', verify_payment),
    (r'^verify_waiver/$', verify_waiver),
    (r'^selectpayment/$', selectpayment),
    (r'^addpayment/$', addpayment),
    (r'^lookup/$', lookup),


    # Mobile
    (r'^combo/$', combo),
    (r'sms/$', sms),
    (r'debug/$', debug),

    # Stats
    (r'^stats/$', stats),
    url(r'^stats/api/', include('stats.urls')),

    # only on local
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
