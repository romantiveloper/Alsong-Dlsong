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
    folders = Myfolder.objects.filter(user_id=user_id)

    data = {'folders':folders, 'user':user}
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

        if len(input_data_list) <= 4:
            return JsonResponse({'status': 'error', 'message': '입력한 리스트의 개수가 4개 이하입니다.'})

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

        
        
@api_view(['GET'])
def recommend_detail(request, list_number):
    user=request.user
    folders = Myfolder.objects.filter(user_id=user, list_number=list_number)
    recommend = Recommend.objects.filter(list_number_id=list_number, user_id=user)

    data = {'recommend':recommend, 'folders':folders}

    return render(request, 'recommend/recommend.html', data)


@api_view(['POST'])
@login_required
def add_recommend(request, list_number):
    if request.method == 'POST':
        data = request.data
        list_number = data['listNumber']
        list_name = data['listName']
        user = request.user
        master_number_id = data['master_number_id']

        print(data)


        song_data = Song.objects.get(master_number=master_number_id)
        print("~~~~~~~~~~~~~~~~~")
        print(song_data)

        # 중복된 데이터 확인
        duplicate_records = Mylist.objects.filter(
            title=song_data.title,
            artist=song_data.artist,
            master_number=master_number_id,
            list_number_id=list_number,
            user=user
        )

        if duplicate_records.exists():
            return JsonResponse({'status':'error', 'message':'이미 추가된 노래입니다.'})

        mylist = Mylist(
            list_name = list_name,
            user = user,
            title = song_data.title,
            artist = song_data.artist,
            cmp = song_data.cmp,
            writer = song_data.writer,
            ky_number_id = song_data.ky_song_num_id,
            tj_number_id = song_data.tj_song_num_id,
            list_number_id = list_number,
            master_number = song_data.master_number
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 500, 'message':'잘못된 요청입니다.'})