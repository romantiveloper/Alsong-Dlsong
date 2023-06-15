from django.db import models

# Create your models here.


class mylist(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    ky_song_num = models.IntegerField()
    tj_song_num = models.IntegerField()

    def __str__(self):
        return self.title