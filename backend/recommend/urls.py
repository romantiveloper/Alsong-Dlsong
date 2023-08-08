from django.urls import path
from .views import recommend, process, recommend_detail,add_recommend


app_name = 'recommend'

urlpatterns = [
    path('', recommend, name="recommend"),
    path('process/', process, name="process"),
    path('<int:list_number>/', recommend_detail, name='mylist_detail'),
    path('<int:list_number>/add-to-recommend/', add_recommend, name="add-to-recommend"),
]