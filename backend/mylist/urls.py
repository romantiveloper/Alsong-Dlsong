from django.urls import path
from .views import mylist,add_list,mylist_detail,DeleteSong, delete_folder,edit_folder,edit_list, add_to_mylist

app_name = 'mylist'

urlpatterns = [
    path('', mylist , name='mylist'),
    path('add_list/', add_list, name='add_list'),
    path('mylist/<int:list_number>/', mylist_detail, name='mylist_detail'),
    path('mylist/delete/', DeleteSong.as_view(), name='delete'),
    path('mylist/deletefolder/', delete_folder, name='delete_folder'),
    path('mylist/editfolder/', edit_folder, name='edit_folder'),
    path('mylist/editlist/', edit_list,name='edit_list'),
    path('add-to-mylist/', add_to_mylist, name='add-to-mylist'),
]
 