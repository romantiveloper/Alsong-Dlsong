from django.urls import path
from .views import mylist,add_list,mylist_detail

app_name = 'mylist'

urlpatterns = [
    path('', mylist , name='mylist'),
    path('add_list/', add_list, name='add_list'),
    path('mylist/<int:list_number>/', mylist_detail, name='mylist_detail'),
]
 