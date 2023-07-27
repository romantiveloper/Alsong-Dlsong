from django.shortcuts import render
from song.models import Song
from mylist.models import Myfolder
from user.models import User
import random
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def recommend(request):
    user_id = request.user
    user = User.objects.filter(user_id=user_id)
    song = Song.objects.all()
    songs = random.sample(list(song), 20)
    folders = Myfolder.objects.filter(user_id=user_id)

    print(user)

    data = {'songs':songs, 'folders':folders, 'user':user}
    return render(request, 'recommend/song.html', data)