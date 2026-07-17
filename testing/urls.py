from django.urls import path
from . import views

urlpatterns = [
    path('', views.router, name='router'),
    path('uploadpost/', views.uploadPost, name='uploadPost'),
    path('feed/', views.feed),
    path('like/', views.like)
]
