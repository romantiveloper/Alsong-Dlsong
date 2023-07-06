from django.shortcuts import render, get_object_or_404
from .models import Mylist, Myfolder
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['GET'])
def mylist(request):
    folder_list = Myfolder.objects.all()
    print(folder_list)
    return render(request, 'main.html', {'folder_list':folder_list})

@api_view(['POST'])
def add_list(request):
    print("add_list 실행")
    list_name = request.POST.get('list_name')
    user = request.user

    Myfolder.objects.create(list_name=list_name, user_id=user.user_id)

    return Response(status=200)

@api_view(['GET'])
def mylist_detail(request, list_number):
    print(list_number)
    data = Mylist.objects.filter(list_number=list_number)
    print(data)
    return render(request, 'songlist/mylist.html', {'data':data})


class DeleteSong(APIView):
    def delete(self, request):
        selected_ids = request.data.get('ids', [])  # 선택된 song.id 값들을 가져옵니다.

        # 선택된 song.id 값들을 기반으로 해당 레코드들을 삭제합니다.
        for song_id in selected_ids:
            mylist = get_object_or_404(Mylist, id=song_id)
            print(mylist)
            
            mylist.delete()

        return Response(status=204)  # 성공적인 삭제 후 응답
