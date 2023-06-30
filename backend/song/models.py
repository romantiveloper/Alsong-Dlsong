from django.db import models

# Create your models here.

#금영 노래
class Kysong(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    song_num = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255, null=True, blank=True, default='none')

    def __str__(self):
        return self.title


#태진 노래
class Tjsong(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    song_num = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255, null=True, blank=True, default='none')
 
    def __str__(self):
        return self.title
    

#전체 노래
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    ky_song_num = models.ForeignKey(Kysong, on_delete=models.CASCADE, related_name='song_set', to_field='song_num')
    tj_song_num = models.ForeignKey(Tjsong, on_delete=models.CASCADE, related_name='song_set', to_field='song_num')

    def __str__(self):
        return self.title
    

#금영 인기 순위
class Ky_pop(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=30, null=True)
    writer = models.CharField(max_length=30, null=True)
    song_num = models.ForeignKey(Kysong, on_delete=models.CASCADE, related_name='kypop_set', to_field='song_num')


#태진 인기 순위
class Tj_pop(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    cmp = models.CharField(max_length=30, null=True)
    writer = models.CharField(max_length=30, null=True)
    song_num = models.ForeignKey(Tjsong, on_delete=models.CASCADE, related_name='tjpop_set', to_field='song_num')

