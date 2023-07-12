from django.urls import path
from .views import recommend

urlpatterns = [
    path('', recommend, name="recommend"),
]