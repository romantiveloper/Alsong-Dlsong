from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('', include('mylist.urls')),
    path("song-list/", include('song.urls')),
    path("user/", include('user.urls')),
    path("recommend/",include('recommend.urls')),
    path("elastic/", include('elastic.urls')),
]


