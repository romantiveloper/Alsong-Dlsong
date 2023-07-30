from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
from django.shortcuts import render
from collections import namedtuple
from mylist.models import Myfolder
  

class SearchView(APIView):
    def get(self, request):
        es = Elasticsearch()

        # 검색어
        query = request.GET.get('query')
        user_id = request.user
        folders = Myfolder.objects.filter(user_id=user_id)
        category = request.GET.get('category')

        print(query)
        print(category)

        if query:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

            if category == 'title':
                docs = es.search(index='song',
                                body={
                                    "query": {
                                        "multi_match": {
                                            "query": query,
                                            "fields": ["title"]
                                        }
                                    }
                                })
            elif category == 'artist':
                docs = es.search(index='song',
                                body={
                                    "query": {
                                        "multi_match": {
                                            "query": query,
                                            "fields": ["artist"]
                                        }
                                    }
                                })

            data_list = docs['hits']
            Song = namedtuple("Song", ["title", "artist", "ky", "tj"])
            results = [Song(x['_source']['title'], x['_source']['artist'], x['_source']['ky_song_num_id'], x['_source']['tj_song_num_id']) for x in data_list['hits']]
        
        else:
           results = []

        print(results)

        data = {'results':results, 'folders':folders}

        return render(request, 'search_results.html', data)
