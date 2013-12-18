from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^config/', include('webconfig.urls')),
    #url(r'^$', lambda x: HttpResponseRedirect('/config/')),
    # url(r'^$', 'bmspanel.views.home', name='home'),
    # url(r'^bmspanel/', include('bmspanel.foo.urls')),
    url(r'^$', RedirectView.as_view(url='/config/')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
