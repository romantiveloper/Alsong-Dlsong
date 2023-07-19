from django.shortcuts import render
from song.models import Song
from mylist.models import Myfolder
import random
# Create your views here.


def recommend(request):
    user_id = request.user
    song = Song.objects.all()
    songs = random.sample(list(song), 20)
    folders = Myfolder.objects.filter(user_id=user_id)

    data = {'songs':songs, 'folders':folders}
    return render(request, 'recommend/song.html', data)