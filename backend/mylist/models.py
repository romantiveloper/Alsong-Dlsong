from django.db import models
from song.models import Kysong, Tjsong, Song
from user.models import User
import random


def list_number():
    return random.randint(100000, 999999)

class Myfolder(models.Model):
    list_name = models.CharField(max_length=30, default='MY 달송')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', default='none')
    list_number = models.IntegerField(primary_key=True, default=list_number)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    song_count = models.IntegerField(default=0)

class Mylist(models.Model):
    list_name = models.CharField(max_length=30, default='노래')
    user= models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', default='none')
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    ky_number = models.ForeignKey(Kysong, on_delete=models.CASCADE, related_name='mylist_set', to_field='song_num')
    tj_number = models.ForeignKey(Tjsong, on_delete=models.CASCADE, related_name='mylist_set', to_field='song_num')
    list_number = models.ForeignKey('Myfolder', on_delete=models.CASCADE, default=1)
    update_date = models.DateTimeField(auto_now=True)
    master_number = models.IntegerField()
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        is_new = True if not self.pk else False
        super(Mylist, self).save(*args, **kwargs)
        if is_new:
            myfolder = self.list_number
            myfolder.song_count = Mylist.objects.filter(list_number=myfolder).count()
            myfolder.save()

    def delete(self, *args, **kwargs):
        myfolder = self.list_number
        super(Mylist, self).delete(*args, **kwargs)
        myfolder.song_count = Mylist.objects.filter(list_number=myfolder).count()
        myfolder.save()