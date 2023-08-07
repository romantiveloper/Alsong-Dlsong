from django.contrib import admin
from django.urls import path, include
from .yasg import *



urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('', include('mylist.urls')),
    path("song-list/", include('song.urls')),
    path("user/", include('user.urls')),
    path("recommend/",include('recommend.urls')),
    path("elastic/", include('elastic.urls')),

    #yasg
    path('swagget<str:format>', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


