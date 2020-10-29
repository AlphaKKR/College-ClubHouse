from django.urls import path
from . import views


urlpatterns = [
    path('uploadcat1', views.uploadCAT1, name='uploadcat1'),
    path('uploadcat2', views.uploadCAT2, name='uploadcat2'),
    path('uploadfat', views.uploadFAT, name='uploadfat'),
    path('uploadsyll', views.uploadSyllabus, name='uploadsyll'),
    path('', views.index, name='index'),
]
