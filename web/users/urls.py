from django.conf.urls import url
from django.contrib.auth.views import login, password_change, password_reset, password_reset_complete, password_reset_confirm, password_reset_done

from users.forms import EmailPasswordResetForm
from users.views import create_user_account, logout_user


urlpatterns = [
    url(r'^login/?$', login, {'template_name': 'users/login.html'}),
    url(r'^logout/?$', logout_user, name='logout_user'),
    url(r'^password-change/?$', password_change, {
        'template_name': 'users/password_change.html',
        'post_change_redirect': '/'}),
    url(r'^password-reset/?$', password_reset, {
        'template_name': 'users/password_reset.html',
        'email_template_name': 'users/password_reset_email.txt',
        'subject_template_name': 'users/password_reset_subject.txt',
        'password_reset_form': EmailPasswordResetForm,
        'post_reset_redirect': '/users/password-reset-done/'}),
    url(r'^password-reset-done/', password_reset_done, {'template_name': 'users/password_reset_done.html'}),
    url(r'^password-reset-complete/', password_reset_complete, {'template_name': 'users/password_reset_complete.html'}),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/?$', password_reset_confirm, {
        'template_name': 'users/password_reset_confirm.html',
        'post_reset_redirect': '/users/password-reset-complete/'
    }, name='password_reset_confirm'),
    url(r'^signup/$', create_user_account, name='create_user_account')
]
