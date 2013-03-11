from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'common.views.hello_world', name='hello_world'),
    url(r'^users/', include('users.urls')),

    # Examples:
    # url(r'^$', 'newdjangosite.views.home', name='home'),
    # url(r'^newdjangosite/', include('newdjangosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
