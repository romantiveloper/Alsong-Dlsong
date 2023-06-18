from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id']
    
    def __str__(self):
        return self.user_id
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        db_table = 'user'
