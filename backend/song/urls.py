from django.urls import path
from .views import song_list, search_view, add_to_search,add_to_tjlist,ky_song_list,add_to_kylist

app_name = 'song'

urlpatterns = [
    path('', song_list, name='song-list'),
    path('ky/',ky_song_list, name='ky_song_list'),
    path('search/', search_view, name='song-search'),
    path('add-to-database/', add_to_search, name='add_to_database'),
    path('add-to-tjlist/', add_to_tjlist, name='add-to-tjlist'),
    path('add-to-kylist/', add_to_kylist, name='add-to-kylist'),
]
