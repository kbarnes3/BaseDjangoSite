from django.urls import path
from django.contrib.auth.views import login, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from users.forms import EmailPasswordResetForm
from users.views import create_user_account, logout_user


urlpatterns = [
    path('login/', login, {'template_name': 'users/login.html'}, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/')),
    # path('password-reset/', PasswordResetView.as_view(
    #     template_name='users/password_reset.html',
    #     email_template_name='users/password_reset_email.txt',
    #     subject_template_name='users/password_reset_subject.txt',
    #     form_class=EmailPasswordResetForm
    # )),
    # path('password-reset-done/', PasswordResetDoneView.as_view(
    #     template_name='users/password_reset_done.html'),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    #     template_name='users/password_reset_confirm.html'
    # ), name='password_reset_confirm'),
    # path('password-reset-complete/', PasswordResetCompleteView.as_view(
    #     template_name='users/password_reset_complete.html'),
    #      name='password_reset_complete'),
    path('signup/', create_user_account, name='create_user_account')
]

