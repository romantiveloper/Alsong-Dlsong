from django.conf.urls import url
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from django.urls import path, include

schema_url_v1_patterns = [
    path('', include('mylist.urls')),
    path("song-list/", include('song.urls')),
    path("user/", include('user.urls')),
    path("recommend/",include('recommend.urls')),
    path("elastic/", include('elastic.urls')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="알쏭달쏭 Open API",
        default_version='v1',
        description="안녕하세요. 알쏭달쏭의 Open API 문서 페이지 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@gmail.com"),
        license=openapi.License(name="알쏭달쏭"),
    ),
    validators=['flex'], #'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)