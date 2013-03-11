from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
    url(r'^logout/$', 'users.views.logout_user', name='logout_user'),
    url(r'^signup/$', 'users.views.create_user_account', name='create_user_account')
)
