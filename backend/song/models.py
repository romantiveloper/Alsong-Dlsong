from django.db import models

# Create your models here.

class kysong(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    song_num = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class tjsong(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    song_num = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255)
 
    def __str__(self):
        return self.title
    

class song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    ky_song_num = models.IntegerField()
    tj_song_num = models.IntegerField()

    def __str__(self):
        return self.title