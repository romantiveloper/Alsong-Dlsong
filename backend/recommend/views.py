from django.shortcuts import render

# Create your views here.


def recommend(request):
    return render(request, 'recommend/song.html')