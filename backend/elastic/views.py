from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
  
from elasticsearch import Elasticsearch  
  
  
class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch()

        # 검색어
        search_word = request.query_params.get('search')

        print(search_word)

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

        docs = es.search(index='song',
                         body={
                             "query": {
                                 "multi_match": {
                                     "query": search_word,
                                     "fields": ["title"]
                                 }
                             }
                         })

        data_list = docs['hits']

        return Response(data_list)