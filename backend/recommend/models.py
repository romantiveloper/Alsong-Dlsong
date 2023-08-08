from django.db import models
from song.models import Song
from user.models import User
from mylist.models import Myfolder


# Create your models here.


class Recommend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', default='none')
    list_number = models.ForeignKey(Myfolder, on_delete=models.CASCADE, default=1)
    master_number = models.ForeignKey(Song, on_delete=models.CASCADE, to_field='master_number')
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    ky_number = models.IntegerField()
    tj_number = models.IntegerField()