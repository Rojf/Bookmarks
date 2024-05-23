from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    # The entry and exit URLs.
    path('', views.dashboard, name='dashboard'),

    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('settings/', views.SettingView.as_view(), name='settings'),
    path('settings/password-change/', views.CustomPasswordChangeView.as_view(), name="password_change"),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url="/account/"),
         name="password_reset_confirm"),

    path('sign-up/', views.UserRegistration.as_view(), name="sign_up"),

    path('users/', views.user_list, name='user_list'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]
