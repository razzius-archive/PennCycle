from django.conf.urls.defaults import patterns, include, url 
from django.conf import settings
from app.views import *
from app.pc_admin import pcAdminSite
from app import api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'penncycle.views.home', name='home'),
    # url(r'^penncycle/', include('penncycle.foo.urls')),

    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^manage/', include(admin.site.urls)),
    url(r'^pc-admin/', include(pcAdminSite.urls)),
    url(r'^admin/', include(pcAdminSite.urls)),
    (r'^$', index),
    (r'^signup/$', signup),
    (r'^faq/$', faq),
    (r'^safety/$', safety),
    (r'^team/$', team),
    (r'^partners/$', partners),
    (r'^locations/$', locations),
    (r'^info_submit/$', info_submit),
    (r'^verify_payment/$', verify_payment),
    (r'^thankyou/(\d{1,8})/$', thankyou),
    (r'^about/(.+)/$', page),
    (r'^verify_waiver/$', verify_waiver),
    (r'^pay/(?P<type>\w+)/(?P<penncard>\d{8})/(?P<plan>\d+)/$', pay),
    (r'^stats/$', stats),
    (r'^selectpayment/$', selectpayment),
    (r'^addpayment/$', addpayment),
    (r'^plans/$', plans),
    (r'^combo/$', combo),
    (r'api/signups/$', api.signups),
    (r'api/schools/$', api.schools),
    (r'api/majors/$', api.majors),
    (r'api/numrides/$', api.numrides),
    (r'api/emails/$', api.emails),
    (r'api/current_emails/$', api.current_emails),
    (r'api/duration/$', api.duration),
    (r'api/gender/$', api.gender),
    (r'api/housing/$', api.housing),
    (r'api/paid/$', api.paid),
    (r'api/year/$', api.year),
    (r'api/payment/$', api.payment),
    (r'api/waived/$', api.waived),
    (r'api/checkouts/$', api.checkouts),
    (r'api/dump/$', api.dump),
    (r'sms/$', sms),
    (r'debug/$', debug),

    #could resurface
    # (r'^events/$', events),

    # django_twilio stuff
    #url(r'^dial/(?P<number>\w+)/$', 'django_twilio.views.dial'),
    #url(r'^dial/?(P<number>\w+)/$', 'django_twilio.views.dial'),

    # url(r'^payment/', payment, name="payment"),
    #(r'^payment/', payment),
    #url(r'^app/', include(app.urls)),
)
