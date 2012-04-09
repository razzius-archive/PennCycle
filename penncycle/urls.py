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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pc-admin/', include(pcAdminSite.urls)),

    (r'^$', index),
    (r'^signup/$', signup),
    (r'^info_submit/$', info_submit),
    (r'^verify_payment/$', verify_payment),
    (r'^thankyou/(\d{8})/$', thankyou),
    (r'^about/(.+)/$', page),
    (r'^verify_waiver/$', verify_waiver),
    (r'^pay/(?P<type>\w+)/(?P<penncard>\d{8})/$', pay),
    (r'^stats/$', stats),
    
    (r'api/signups/$', api.signups),
    (r'api/schools/$', api.schools),
    (r'api/majors/$', api.majors),

    # django_twilio stuff
    #url(r'^dial/(?P<number>\w+)/$', 'django_twilio.views.dial'),
    #url(r'^dial/?(P<number>\w+)/$', 'django_twilio.views.dial'),

    # url(r'^payment/', payment, name="payment"),
    #(r'^payment/', payment),
    #url(r'^app/', include(app.urls)),
)
