from django.conf.urls import patterns, url
from django.contrib import admin
from webconfig import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #edit
    url(r'^(?P<config_id>\d+)/edit$', views.editpoint, name='editpoint'),
    #delete
    url(r'^(?P<config_id>\d+)/delete$', views.deletepoint, name='deletepoint'),
    url(r'^add', views.addpoint, name='addpoint'),
    url(r'^reboot', views.reboot, name='reboot'),
    url(r'^debug', views.debug, name='debug'),
    url(r'^scanlist', views.scanlist, name='scanlist'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
    'template_name': 'webconfig/login.html'
}),
    #url(r'^login', views.loginpage, name='loginpage'),
)
