from django.shortcuts import render
from .models import mylist
# Create your views here.

def mylist(request):
    return render(request, 'main.html')