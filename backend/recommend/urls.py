from django.urls import path
from .views import recommend, process

urlpatterns = [
    path('', recommend, name="recommend"),
    path('process/', process, name="process"),
]