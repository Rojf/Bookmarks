from django.urls import path

from images import views


app_name = 'images'

urlpatterns = [
    path('create/', views.ImageCreateViews.as_view(), name='create'),
]
