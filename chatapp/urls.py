from django.urls import path
from . import views


urlpatterns = [
    path('', views.chathome, name='chathome'),
    path('<room_name>/', views.activeroom, name='activeroom'),
    path('messages', views.Messages, name='messages'),
    path('post', views.Post, name='post'),
]
