from django.db import models

# Create your models here.

#금영 노래
class Kysong(models.Model):
    song_num = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    master_title = models.CharField(max_length=255,null=True, blank=True, default='none')
    master_singer = models.CharField(max_length=255,null=True, blank=True, default='none')
    play = models.CharField(max_length=255,null=True, blank=True, default='none')
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    genre = models.CharField(max_length=255, null=True, blank=True, default='none')

    def __str__(self):
        return self.title


#태진 노래
class Tjsong(models.Model):
    song_num = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    master_title = models.CharField(max_length=255,null=True, blank=True, default='none')
    master_singer = models.CharField(max_length=255,null=True, blank=True, default='none')
    play = models.CharField(max_length=255,null=True, blank=True, default='none')
    cmp = models.CharField(max_length=255, null=True, blank=True, default='none')
    writer = models.CharField(max_length=255, null=True, blank=True, default='none')
    key = models.CharField(max_length=255, null=True, blank=True, default='none')
    genre = models.CharField(max_length=255, null=True, blank=True, default='none')
    
    
    def __str__(self):
        return self.title
    
#전체 노래
class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    cmp = models.TextField(max_length=255, null=True, blank=True, default='none')
    writer = models.TextField(max_length=255, null=True, blank=True, default='none')
    ky_song_num = models.ForeignKey(Kysong, on_delete=models.CASCADE, related_name='song_set', to_field='song_num')
    tj_song_num = models.ForeignKey(Tjsong, on_delete=models.CASCADE, related_name='song_set', to_field='song_num')
    master_title = models.TextField(max_length=255, null=True, blank=True, default='none')
    master_singer = models.TextField(max_length=255, null=True, blank=True, default='none')
    play = models.TextField(max_length=255, null=True, blank=True, default='none')
    제목_KY = models.TextField(max_length=255, null=True, blank=True, default='none')
    가수_KY = models.TextField(max_length=255, null=True, blank=True, default='none')
    melon_tj = models.TextField(max_length=255, null=True, blank=True, default='none')
    genre = models.TextField(max_length=255, null=True, blank=True, default='none')
    master_number = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.title
    

#금영 인기 순위
class Ky_pop(models.Model):
    rank = models.IntegerField()
    title = models.TextField(max_length=255)
    artist = models.TextField(max_length=255)
    # cmp = models.TextField(max_length=255, null=True, blank=True, default='none')
    # writer = models.TextField(max_length=255, null=True, blank=True, default='none')
    id = models.IntegerField(primary_key=True)
    song_num_id = models.IntegerField()


#태진 인기 순위
class Tj_pop(models.Model):
    rank = models.IntegerField()
    title = models.TextField(max_length=255)
    artist = models.TextField(max_length=255)
    # cmp = models.TextField(max_length=255, null=True, blank=True, default='none')
    # writer = models.TextField(max_length=255, null=True, blank=True, default='none')
    id = models.IntegerField(primary_key=True)
    song_num_id = models.IntegerField()