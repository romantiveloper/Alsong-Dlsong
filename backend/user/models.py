from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField()
    email = models.EmailField()
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField()
    role = models.CharField(max_length=10)
