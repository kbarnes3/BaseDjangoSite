from django.urls import path
from django.contrib.auth.views import login, password_reset, password_reset_complete, password_reset_confirm, password_reset_done, PasswordChangeView

from users.forms import EmailPasswordResetForm
from users.views import create_user_account, logout_user


urlpatterns = [
    path('login/', login, {'template_name': 'users/login.html'}, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('password-change/', PasswordChangeView.as_view(template_name='users/password_change.html', success_url='/')),
    path('password-reset/', password_reset, {
        'template_name': 'users/password_reset.html',
        'email_template_name': 'users/password_reset_email.txt',
        'subject_template_name': 'users/password_reset_subject.txt',
        'password_reset_form': EmailPasswordResetForm,
        'post_reset_redirect': '/users/password-reset-done/'}),
    path('password-reset-done/', password_reset_done, {'template_name': 'users/password_reset_done.html'}),
    path('password-reset-complete/', password_reset_complete, {'template_name': 'users/password_reset_complete.html'}),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, {
        'template_name': 'users/password_reset_confirm.html',
        'post_reset_redirect': '/users/password-reset-complete/'
    }, name='password_reset_confirm'),
    path('signup/', create_user_account, name='create_user_account')
]
