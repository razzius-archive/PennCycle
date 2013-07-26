from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

from app.views import *
from app.dump import dump
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
    (r'^welcome/$', welcome),
    (r'^safety/$', Safety),

    # Backend-related
    (r'^verify_payment/$', verify_payment),
    (r'^verify_waiver/$', verify_waiver),
    (r'^verify_pin/$', verify_pin),
    (r'^lookup/$', lookup),
    (r'^bursar/$', bursar),
    (r'^credit/$', credit),
    (r'^dump/$', dump),

    # Mobile
    (r'^combo/$', combo),
    (r'^sms/$', sms),
    (r'^debug/$', debug),
    (r'^send_pin/$', send_pin),

    # Stats
    (r'^stats/$', Stats.as_view()),
    url(r'^stats/api/', include('stats.urls')),

    # only on local
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
