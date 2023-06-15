from django.shortcuts import render
from .models import kysong, tjsong, song
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.

def song_list(request):
    if request.method == 'POST':  
        category = request.POST.get('category')
        if category == 'TJ':
            songs = tjsong.objects.all()
        elif category == 'KY':
            songs = kysong.objects.all()
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

        results = song.objects.filter(conditions)

    else:
        results = []
    
    # 검색 결과 처리
    # ...

    print(results)

    return render(request, 'songlist/search.html', {'results': results})


