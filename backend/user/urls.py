from django.urls import path
from .views import Login, Join
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('join/', Join.as_view(), name='join'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),   
    # path('/login/kakao', ), # 일단 API 설계에 따라 path 틀만 짜둠
    # path('/login/naver', ), # 일단 API 설계에 따라 path 틀만 짜둠
]
