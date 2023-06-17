from django.db import models
from song.models import kysong, tjsong
from user.models import User

class myfolder(models.Model):
    list_name = models.CharField(max_length=30, default='노래')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')
    list_number = models.IntegerField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.ForeignKey('mylist', on_delete=models.CASCADE)

class mylist(models.Model):
    list_name = models.CharField(max_length=30, default='노래')
    user= models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', default='none')
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    ky_number = models.ForeignKey(kysong, on_delete=models.CASCADE, related_name='mylist_set', to_field='song_num')
    tj_number = models.ForeignKey(tjsong, on_delete=models.CASCADE, related_name='mylist_set', to_field='song_num')
    list_number = models.ForeignKey('myfolder', on_delete=models.CASCADE, default=1)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
