from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
# from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = 'user'
    GENDER_MAIL = 'Male'
    GENDER_FEMAIL = 'Female'
    GENDER_CHOICES = ((GENDER_MAIL, 'Male'),(GENDER_FEMAIL, 'Female'))
    LOGIN_EMAIL = 'email'
    LOGIN_KAKAO = 'kakao'
    #favorite_movies = models.ManyToManyField(mv_models.Movie,blank=True, related_name='users')
    LOGIN_CHOICES = ((LOGIN_EMAIL,'Email'),(LOGIN_KAKAO, 'Kakao'))
    user_id = models.CharField(max_length=30,blank=True, unique=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default=GENDER_MAIL)
    nickname = models.CharField(max_length=30,blank=True)
    profile_img = models.ImageField(upload_to='profile_img/',default='https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png')
    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=20, default=LOGIN_EMAIL)
    
    # 에러 해결용
    
    # constraints = [
    #         models.UniqueConstraint(fields=['user_id'], name='unique_user_id')
    #     ]
