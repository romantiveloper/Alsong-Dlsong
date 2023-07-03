from django.urls import path, include
from . import views
from mylist.views import mylist

app_name = 'user'

urlpatterns = [
    path('',views.base, name='base'),
    path('main/',views.main, name='home'), # 메인페이지(top10, user님 취향에 맞는 콘텐츠)로 랜딩
    path('sign-up/', views.sign_up_view, name='sign-up'), # 회원가입 페이지로 랜딩
    path('sign-in/', views.sign_in_view, name='sign-in'), # 로그인 페이지로 랜딩
    path('kakao/', views.to_kakao, name='kakao'), # 카카오 로그인 하기
    path('kakao/callback/', views.from_kakao, name='kakako_login'), # 카카오 로그인에서 정보 가져오기
    path('logout/', views.log_out, name='logout'), # 로그아웃
    path('mypage/',views.my_page, name='mypage'), # 마이페이지
    #path('pwchange/',views.pw_change, name='pwchange'), # 비밀번호 변경
    #path('idchange/', views.id_change, name='idchange'), # 아이디 변경
    #path('email_ajax/',views.email_ajax, name='email_ajax'), # 인증 메일 보내기
    #path('certify_ajax/',views.certify_ajax, name='certify_ajax'), # 인증번호 확인
    path('isid/',views.is_id, name='is_id'), # 임시 비밀번호 발급(아이디는 알고 비번은 모를 때)
    #path('my-modify/',views.my_modify, name='my_modify'), # 프로필 이미지 수정
    #path('birth-change/', views.birth_change, name='birth-change'), # 생년월일 수정
    #path('gender-change/', views.gender_change, name='gender-change'), #성별 수정
    #path('like-or-donlike/',views.like_or_donlike,name='like_or_donlike'), # 좋아요 싫어요
]


