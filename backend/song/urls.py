from django.urls import path
from .views import song_list, search_view, add_to_database

app_name = 'song'

urlpatterns = [
    path('', song_list, name='song-list'),
    path('search/', search_view, name='song-search'),
    path('add-to-database/', add_to_database, name='add_to_database'),
]
