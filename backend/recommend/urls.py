from django.urls import path
from .views import recommend, process, recommend_detail


app_name = 'recommend'

urlpatterns = [
    path('', recommend, name="recommend"),
    path('process/', process, name="process"),
    path('<int:list_number>/', recommend_detail, name='mylist_detail'),
]