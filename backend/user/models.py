from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('user_id 필드가 비어 있습니다.')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id, password, **extra_fields)

class User(AbstractUser):
    
    class Meta:
        db_table = 'user'

    objects = CustomUserManager()
        
    id = models.AutoField(primary_key = True) # 일련번호 id
    
    GENDER_MAIL = 'Male'
    GENDER_FEMAIL = 'Female'
    GENDER_CHOICES = ((GENDER_MAIL, 'Male'),(GENDER_FEMAIL, 'Female')) # 성별 선택 항목 생성
    
    LOGIN_EMAIL = 'email'
    LOGIN_KAKAO = 'kakao'
    LOGIN_CHOICES = ((LOGIN_EMAIL,'Email'),(LOGIN_KAKAO, 'Kakao')) # 로그인 방식 항목 생성
    
    user_id = models.CharField(max_length=40,blank=True, unique=True) # 로그인용 id
    USERNAME_FIELD = 'user_id' # django의 기본 User 모델에서 username으로 user_id 사용하겠다고 명시 커스텀
    
    nickname = models.CharField(max_length=30,blank=True) # 닉네임
    birthday = models.DateField(blank=True, null=True) # 생년월일
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default=GENDER_MAIL) # 성별
    profile_img = models.ImageField(upload_to='profile_img/',default='static/img/user_default.png') # 프로필 사진
    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=20, default=LOGIN_EMAIL) # 로그인 정보(이메일/카카오)

    
