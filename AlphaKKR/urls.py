from django.contrib import admin
from django.urls import path, include
from homepage.views import Profile
from chatapp.views import createroom


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', Profile, name='profile'),
    path('', include('homepage.urls')),
    path('resources/', include('resources.urls')),
    path('clubs/', include('clubs.urls')),
    path('chatroom/', include('chatapp.urls')),
    path('createroom/', createroom, name='createroom')
]
