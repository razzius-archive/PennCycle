from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.http import HttpResponse
admin.autodiscover()

from app.views import *
from app.dump import dump
from mobile.views import sms, send_pin

urlpatterns = patterns(
    '',
    url(r'^manage/', include(admin.site.urls)),
    url(r'^admin/', include('staff.urls')),
    url(r'^admin-login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Normal pages
    (r'^$', Index.as_view()),
    (r'^signup/$', Signup.as_view()),
    (r'^signin/$', login, {"template_name": "signin.html"}),
    (r'^login/$', login, {"template_name": "signin.html"}),
    (r'^faq/$', Faq.as_view()),
    (r'^safety/$', Safety.as_view()),
    (r'^about/$', About.as_view()),
    (r'^locations/$', Locations.as_view()),
    (r'^welcome/$', welcome),
    (r'^safety/$', Safety),
    (r'^about/$', Index.as_view()),

    # Backend-related
    (r'^verify_payment/$', verify_payment),
    (r'^verify_waiver/$', verify_waiver),
    (r'^verify_pin/$', verify_pin),
    (r'^lookup/$', lookup),
    (r'^bursar/$', bursar),
    (r'^credit/$', credit),
    (r'^cash/$', cash),
    (r'^dump/$', dump),
    (r'^combo/$', combo),

    # Twilio
    (r'^sms/$', sms),

    # Mobile
    url(r'^mobile/', include('mobile.urls')),
    (r'^send_pin/$', send_pin),

    # Stats
    (r'^stats/$', Stats.as_view()),
    url(r'^stats/api/', include('stats.urls')),

    # misc
    url(r'favicon.ico', 'django.views.static.serve', {'document_root': '/static/img/favicon.ico'),

    # only on local
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain"))
)
