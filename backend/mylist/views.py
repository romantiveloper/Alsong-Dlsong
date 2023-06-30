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
    data = get_object_or_404(Myfolder, list_number=list_number)
    return render(request, 'songlist/mylist.html', {'data':data})

