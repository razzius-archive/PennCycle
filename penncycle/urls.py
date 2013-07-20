from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

from app.views import *
from mobile.views import sms, debug, send_pin

urlpatterns = patterns(
    '',
    url(r'^manage/', include(admin.site.urls)),
    url(r'^admin/', include('staff.urls')),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    # Normal pages
    (r'^$', Index.as_view()),
    (r'^signup/$', Signup.as_view()),
    (r'^signin/$', login, {"template_name": "signin.html"}),
    (r'^faq/$', Faq.as_view()),
    (r'^safety/$', Safety.as_view()),
    (r'^team/$', Team.as_view()),
    (r'^locations/$', Locations.as_view()),
    (r'^plans/$', Plans.as_view()),
    (r'^welcome/$', welcome),
    (r'^safety/$', Safety),
    (r'^thankyou/(?P<penncard>\d{1,8})/$', thankyou),
    (r'^pay/(?P<payment_type>\w+)/(?P<penncard>\d{8})/(?P<plan>\d+)/$', pay),
    (r'^select_payment/$', select_payment),

    # Backend-related
    (r'^verify_payment/$', verify_payment),
    (r'^verify_waiver/$', verify_waiver),
    (r'^verify_pin/$', verify_pin),
    (r'^addpayment/$', addpayment),
    (r'^lookup/$', lookup),

    # Mobile
    (r'^combo/$', combo),
    (r'sms/$', sms),
    (r'debug/$', debug),
    (r'send_pin/$', send_pin),

    # PhoneGap
    (r'^api/', include('api.urls')),

    # Stats
    (r'^stats/$', Stats.as_view()),
    url(r'^stats/api/', include('stats.urls')),

    # only on local
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
