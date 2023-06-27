from django.shortcuts import render
# from .models import Mylist
# Create your views here.

def mylist(request):
    return render(request, 'main.html')