from django.conf.urls import patterns, url

from users.forms import EmailPasswordResetForm


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
    url(r'^logout/$', 'users.views.logout_user', name='logout_user'),
    url(r'^password-change/?$', 'django.contrib.auth.views.password_change', {
        'template_name': 'users/password_change.html',
        'post_change_redirect': '/'}),
    url(r'^password-reset/?$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'users/password_reset.html',
        'email_template_name': 'users/password_reset_email.txt',
        'subject_template_name': 'users/password_reset_subject.txt',
        'password_reset_form': EmailPasswordResetForm,
        'post_reset_redirect': '/users/password-reset-done/'}),
    url(r'^password-reset-done/', 'django.contrib.auth.views.password_reset_done', {'template_name': 'users/password_reset_done.html'}),
    url(r'^password-reset-complete/', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/password_reset_complete.html'}),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/?$', 'django.contrib.auth.views.password_reset_confirm', {
        'template_name': 'users/password_reset_confirm.html',
        'post_reset_redirect': '/users/password-reset-complete/'
    }, name='password_reset_confirm'),
    url(r'^signup/$', 'users.views.create_user_account', name='create_user_account')
)
