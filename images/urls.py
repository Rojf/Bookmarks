from django.urls import path

from images import views


app_name = 'images'

urlpatterns = [
    path('', views.images_list, name='list'),
    path('create/', views.ImageCreateViews.as_view(), name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
]
