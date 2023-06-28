from django.shortcuts import render
from .models import Kysong, Tjsong, Song
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from mylist.models import Mylist, Myfolder
import json
# Create your views here.

def song_list(request):
    if request.method == 'POST':  
        category = request.POST.get('category')
        if category == 'TJ':
            songs = Tjsong.objects.all()
        elif category == 'KY':
            songs = Kysong.objects.all()
        else:
            songs = []
    else:
        songs = []
    
    print(songs)

    return render(request, 'songlist/song-list.html', {'songs': songs})



def search_view(request):
    query = request.GET.get('query')
    
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

    return render(request, 'songlist/search.html', {'results': results})


def add_to_database(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # 전송된 데이터 파싱

        # 데이터베이스에 값을 추가하는 로직
        mylist = Mylist(
            ky_number_id=data['kySongNum'],
            tj_number_id=data['tjSongNum'],
            title=data['title'],
            artist=data['artist'],
            cmp=data['cmp'],
            writer=data['writer']
        )
        mylist.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})