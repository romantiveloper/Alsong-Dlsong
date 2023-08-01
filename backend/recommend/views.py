from django.shortcuts import render
from song.models import Song
from mylist.models import Myfolder, Mylist
from user.models import User
import random
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import Recommend
from rest_framework.decorators import api_view

# Create your views here.

@login_required
def recommend(request):
    user_id = request.user
    user = User.objects.filter(user_id=user_id)
    song = Song.objects.all()
    songs = random.sample(list(song), 20)
    folders = Myfolder.objects.filter(user_id=user_id)

    data = {'songs':songs, 'folders':folders, 'user':user}
    return render(request, 'recommend/song.html', data)


@api_view(['POST'])
@login_required
@csrf_exempt
def process(request):
    if request.method == 'POST':
        data = request.data
        user = request.user
        list_number = data['listNumber']

        print(list_number)

        input_data = Mylist.objects.filter(list_number_id=list_number, user_id=user).values("master_number","list_number_id","user_id" )
        input_data_list = list(input_data) 

        print(input_data_list)

        fastapi_service_url = 'http://34.64.174.219:8001/process'
        response = requests.post(fastapi_service_url, json={"input_data": input_data_list})
        result = response.json()['result']

        print(result)

        Recommend.objects.filter(list_number_id=list_number, user_id=user).delete()
        
        for x in result:
            recommend = Recommend(
                title=x['title'],
                artist=x['artist'],
                ky_number=x['ky_song_num_id'],
                tj_number=x['tj_song_num_id'],
                master_number_id=x['master_number'],
                list_number_id=list_number,
                user_id=user
            )

            recommend.save()

        return JsonResponse({'status': 'success'})

        
        
