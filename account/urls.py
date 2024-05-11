from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Custom login url.
    # path('login/', views.UserLoginView.as_view(), name='login'),

    # The entry and exit URLs.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
