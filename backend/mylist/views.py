from django.shortcuts import render, get_object_or_404
from .models import Mylist, Myfolder
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from recommend.models import Recommend
from user.models import User
from song.models import Song


# Create your views here.


@api_view(['GET'])
def mylist(request):
    user_id = request.user
    folder_list = Myfolder.objects.filter(user_id=user_id)
    user = User.objects.filter(user_id=user_id)
    print(folder_list)
    print(user_id)
    
    song_count = Myfolder.objects.filter(user_id=user_id).values("song_count")
    print(song_count)

    total=[]

    for x in song_count:
        song=x['song_count']
        total.append(song)
        print(type(song))

    print(sum(total))
    total_song = sum(total)
    data = {'folder_list':folder_list, 'user':user, 'total_song':total_song}
    return render(request, 'main.html', data)



@api_view(['POST'])
def add_list(request):
    print("add_list 실행")
    list_name = request.POST.get('list_name')
    user = request.user
    print(list_name)

    Myfolder.objects.create(list_name=list_name, user_id=user.user_id)

    return Response(status=200)



@api_view(['GET'])
def mylist_detail(request, list_number):
    print(list_number)
    user=request.user
    lists = Mylist.objects.filter(list_number=list_number)
    folders = Myfolder.objects.filter(list_number=list_number)
    recommend = Recommend.objects.filter(list_number_id=list_number, user_id=user)[:3]


    data = {'lists':lists, 'folders':folders, 'recommend':recommend}
    return render(request, 'songlist/mylist.html', data)


class DeleteSong(APIView):
    def delete(self, request):
        selected_ids = request.data.get('ids', [])  # 선택된 song.id 값들을 가져옵니다.

        # 선택된 song.id 값들을 기반으로 해당 레코드들을 삭제합니다.
        for song_id in selected_ids:
            mylist = get_object_or_404(Mylist, id=song_id)
            print(mylist)
            
            mylist.delete()

        return Response(status=204)  # 성공적인 삭제 후 응답


@api_view(['POST'])
def delete_folder(request):
    list_number = request.data.get('list_number')
    print(list_number)
    try:
        folder = Myfolder.objects.get(list_number=list_number)
        folder.delete()
        return JsonResponse({'message': '폴더가 성공적으로 삭제되었습니다.'})
    except Myfolder.DoesNotExist:
        return JsonResponse({'message': '폴더를 찾을 수 없습니다.'}, status=501)
    

@api_view(['POST'])
def edit_folder(request):
    list_name = request.data.get('newFolderName')
    list_number = request.data.get('listNumber')
    print(list_name)
    print(list_number)

    try:
        folder = Myfolder.objects.get(list_number=list_number)
        folder.list_name = list_name
        folder.save()

        return JsonResponse({'success':True})
    
    except Myfolder.DoesNotExist:
        return JsonResponse({'success':False, 'error':'폴더를 찾을 수 없습니다.'}, status=404)

@api_view(['POST'])
def edit_list(request):
    new_list_name = request.data.get('newFolderName')
    list_number = request.data.get('listNumber')
    old_list_name = request.data.get('listName')
    print(new_list_name)
    print(list_number)

    try:
        # 기존 list_name을 가진 모든 Myfolder 객체와 Mylist 객체를 가져옵니다.
        lists = Mylist.objects.filter(list_name=old_list_name)

        if lists.exists():
            for list in lists:
                list.list_name = new_list_name
                list.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '기존 폴더를 찾을 수 없습니다.'}, status=404)

        

    except Mylist.DoesNotExist:
        return JsonResponse({'success': False, 'error': '폴더를 찾을 수 없습니다.'}, status=404)


@api_view(['POST'])
@login_required
def add_to_mylist(request):
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