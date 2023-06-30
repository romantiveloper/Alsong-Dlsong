from django.shortcuts import render
from .models import Kysong, Tjsong, Song,Ky_pop,Tj_pop
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from mylist.models import Mylist, Myfolder
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def song_list(request):
    if request.method == 'POST':  
        category = request.POST.get('category')
        if category == 'TJ':
            songs = Tj_pop.objects.all()
        elif category == 'KY':
            songs = Ky_pop.objects.all()
        else:
            songs = []
    else:
        songs = []
    
    print(songs)

    return render(request, 'songlist/song-list.html', {'songs': songs})



def search_view(request):
    query = request.GET.get('query')
    folders = Myfolder.objects.all()
    
    print(query)

    if query:
        words = query.split()  # 검색어를 공백으로 분리하여 단어 리스트 생성

        # 쿼리 조건 생성
        conditions = Q()
        for word in words:
            conditions |= Q(title__icontains=word)  # 대소문자 구분 없이 단어 포함 여부 검색

        results = Song.objects.filter(conditions)

    else:
        results = []
    
    # 검색 결과 처리
    # ...

    print(results)

    data = {'results': results, 'folders':folders}
    return render(request, 'songlist/search.html', data)


@login_required
def add_to_database(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 현재 로그인한 사용자 정보 가져오기
        user = request.user

        # 선택한 My_folder의 list_number와 list_name 가져오기
        list_number = data['listNumber']
        list_name = data['listName']

        # 데이터베이스에 값을 추가하는 로직
        mylist = Mylist(
            list_name=list_name,
            user=user,
            title=data['title'],
            artist=data['artist'],
            cmp=data['cmp'],
            writer=data['writer'],
            ky_number_id=data['kySongNum'],
            tj_number_id=data['tjSongNum'],
            list_number_id=list_number
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})