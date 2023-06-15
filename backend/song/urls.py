from django.urls import path
from .views import song_list, search_view

app_name = 'song'

urlpatterns = [
    path('', song_list, name='song_list'),
    path('search/', search_view, name='song_search'),
]
