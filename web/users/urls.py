from django.urls import include, path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView

from users.forms import EmailPasswordResetForm
from users.views import create_user_account


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/')),
    path('password_reset/', PasswordResetView.as_view(form_class=EmailPasswordResetForm), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', create_user_account, name='create_user_account')
]

