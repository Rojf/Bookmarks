from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    # Custom login url.
    # path('login/', views.UserLoginView.as_view(), name='login'),

    # The entry and exit URLs.
    path('', views.dashboard, name='dashboard'),
    path('images', views.images, name='images'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
