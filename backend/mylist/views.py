from django.shortcuts import render
from .models import Mylist, Myfolder
# Create your views here.

def mylist(request):
    forder_list = Myfolder.objects.all()
    print(forder_list)
    return render(request, 'main.html', {'forder_list':forder_list})