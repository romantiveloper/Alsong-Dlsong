from django.urls import path
from .views import mylist

app_name = 'mylist'

urlpatterns = [
    path('',mylist , name='mylist'),
]
