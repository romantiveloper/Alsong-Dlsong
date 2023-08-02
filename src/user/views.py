import json
with open('secrets.json') as f:
    secrets = json.loads(f.read())
import random
import string
import datetime
from random import randint
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect, reverse
from . import models
from .models import User
from django.contrib import auth, messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import uuid
from .utils import parse_birthday
from django.conf import settings
from django.http import HttpResponseRedirect


# 가입 유도하는 페이지(landing.html)로의 랜딩부
def base(request):
    user = request.user.is_authenticated # 가입한 사람인지 확인
    # True, False반환
    if not user: # 가입 안 한 사람이라면
        return render(request, 'landing.html') # 가입 유도 랜딩 페이지로
    return redirect('/') # 가입 한 사람이면 그냥 일반 메인 페이지로


#@login_required # 로그인 된 사람
def main(request): 
    print('로그인 된 사람') 
    return render(request, 'main.html') # 일반 메인 페이지로 랜딩


certify = False # 메일 인증 상태 False로 초기화

# 회원가입
def sign_up_view(request):
    print('회원가입 시도') #인증번호
    global certify # 메일 인증 상태에 대한 변수 'certify'를 전역변수로 선언
    if request.method == 'GET':  # 요청이 get으로 들어온다면
        is_user = request.user.is_authenticated # 가입된 유저인지 여부 request 요청, 결과를 is_user 변수에 저장
        if is_user: # 가입 여부 True라면
            return redirect('/') # 메인 페이지로 리다이렉트

        return render(request, 'user/signup.html') # get에 대한 리턴으로 signup.html로 랜딩함

    elif request.method == 'POST':  # 요청이 post로 들어온다면
        global certify_num
        data = json.loads(request.body.decode('utf-8')) # POST 요청에서 전달받은 본문(body) 가져와 "data"라는 변수에 저장, JSON 형식의 문자열을 딕셔너리로 변환
        username = data['username'] 
        user_id = data['user_id'] 
        password1 = data['password1']
        password2 = data['password2']
        nickname = data['nickname']
        email = data['email']
        birthday = data['birthday']
        gender = data['gender']
 
        err_msg = '' # 에러 메시지 초기화

        # user_id = str(uuid.uuid4())

        if username == '': # 이름 공백일 때
            err_msg = '이름을 적어주세요.'
        if user_id == '' or password1 == '': # 아이디/비번 공백으로 로그인 시도 때
            err_msg = '아이디 및 패스워드를 확인해주세요'
        if nickname == '': # 닉네임 공백일 때
            err_msg = '닉네임을 적어주세요.'
        if email == '': # 이메일 공백일 때
            err_msg = '이메일을 적어주세요.'
        if birthday == '': # 생일 공백일 때
            err_msg = '생년월일을 적어주세요.'
        if gender == '1': # 성별 디폴트값일 때
            err_msg = '성별을 적어주세요.'
        if password1 != password2: # 비번과 비번 확인이 다를 때
            err_msg = '비밀번호가 일치하지 않습니다.'
        # if not certify: # 이메일 인증 하지 않았을 때
        #     err_msg = '이메일을 인증해주세요.'
            
        is_it = get_user_model().objects.filter(user_id=user_id) # 지금 POST 요청에서 받은 user_id과 기존 DB의 user_id이 일치할 경우
        is_it2 = get_user_model().objects.filter(email=email) # 지금 POST 요청에서 받은 email과 기존 DB의 email이 일치할 경우
        
        if is_it:
            err_msg = '사용자가 존재합니다.'
        if is_it2:
            err_msg = '이메일이 중복됩니다.'
        
        
        # context 변수: 오류 메시지를 포함하는 딕셔너리를 만들고, 그것을 클라이언트에게 JSON 형태로 반환하기 위해 사용
        context = {'error': err_msg} 
        
        if len(err_msg) > 1: # 만약 err_msg가 빈 문자열이 아니라면, 오류 발생한 것으로 간주
            return JsonResponse(context) # 'error' 키와 함께 err_msg가 포함된 딕셔너리를 json 형식으로 응답으로 보내줌

        # get_user_model() 함수: Django에서 제공하는 내장 함수로서, 장고의 auth 앱에서 사용자 모델을 가져오는 역할
        get_user_model().objects.create_user(username=username, user_id=user_id, password=password1, nickname=nickname, 
                                             email=email, birthday=birthday, gender=gender)
       
       # 다 끝나면 회원가입 완료 처리
        context = {'ok': '회원가입완료'}
        return JsonResponse(context)


# 로그인
def sign_in_view(request): 
    if request.method == 'POST':
        user_id = request.POST.get('user_id') 
        password = request.POST.get('password')
        me = auth.authenticate(request, user_id=user_id, password=password) # 장고의 auth 앱 사용, 사용자 ID/PW 확인
        print("로그인 시도")
        if not me:  # ID/PW 맞지 않는다면
            return render(request, 'user/signin.html', {'error': '아이디 혹은 비밀번호가 틀렸습니다.'}) # 에러 발생 후 로그인 창으로 랜딩
        auth.login(request, me) # ID/PW 잘 맞는다면, me 정보로 로그인
        return redirect('/') # 로그인 된 채로 main 페이지로 랜딩
    else: 
        is_user = request.user.is_authenticated 
        if is_user:
            return redirect('/')
        return render(request, 'user/signin.html')
    

# 로그아웃
@login_required
def log_out(request):
    auth.logout(request) # 장고의 auth 앱 사용, 로그아웃
    messages.success(request, '로그아웃이 완료되었습니다👌🏻')
    return redirect('/')


# (admin용) 회원 관리 페이지
@login_required
def user_view(request):
    if request.method == 'GET':
        user_list = User.objects.all().exclude(user_id=request.user.user_id)
        return render(request, 'user/user_list.html', {'user_list': user_list})



# 카카오 로그인 시도
def to_kakao(request):
    REST_API_KEY = secrets['REST_API_KEY']
    REDIRECT_URI = 'http://35.216.62.167/user/kakao/callback'
    
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code')


# 카카오 로그인에서 필요 정보 가져오기
def from_kakao(request):
    REST_API_KEY = secrets['REST_API_KEY']
    REDIRECT_URI = 'http://35.216.62.167/user/kakao/callback'
    code = request.GET.get('code', 'None')
    if code is None:
        # 코드 발급 x일 경우
        return redirect('/')
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    data = {
        'client_id': REST_API_KEY,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code',
    }
    response = requests.post('https://kauth.kakao.com/oauth/token', headers=headers, data=data)
    res_dict = response.json() 
    if 'error' in res_dict or 'access_token' not in res_dict:
        # 에러 발생 처리
        return redirect('/')
    access_token = res_dict.get('access_token', None)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    res_dict = response.json()
    
    kakao_account = res_dict.get('kakao_account')
    user_id = res_dict.get('id')
    properties = res_dict.get('properties')

    username = res_dict.get('id')
    email = res_dict.get('kakao_account', {}).get('email', None)
    uid = 'kakao_{}'.format(res_dict.get('id'))
    
    #username = properties.get('nickname', None)
    nickname = res_dict.get('kakao_account', {}).get('profile', {}).get('nickname', 'Unknown')
    profile_img = properties.get('profile_image', None)
    gender = kakao_account.get('gender', None)
    birthday = kakao_account.get('birthday', None)
    modified_birthday = parse_birthday(birthday)
    #email = kakao_account.get('email', None)
    
    
    if email is None:
        # 이메일 동의 안하면 로그인 불가 처리
        print('이메일 없이는 가입이 불가해요😢')
        return redirect('/user/sign-in')
    
    try:
        user = get_user_model().objects.get(email=email)

        if user.login_method != models.User.LOGIN_KAKAO:
            print('카카오로 가입하지 않은 다른 아이디가 존재합니다😲')
            return redirect('/user/sign-in')


    except:
        user = models.User.objects.create(user_id=user_id, username=username, nickname=nickname, profile_img=profile_img, 
                                   email=email, login_method=models.User.LOGIN_KAKAO, birthday=modified_birthday, gender=gender)

        user.set_unusable_password()
        user.save()

    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


@login_required
def my_page(request):
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print(request.method)
    if request.method == 'POST':
        pass
    else:
        user = request.user
        print(user)
        print(user.username)
        err = False
        if user.login_method != 'email' and (user.birthday is None or user.gender is None):
            err = '카카오톡으로 로그인 하신 경우에는 반드시 생일, 성별을 설정해주세요!'
        return render(request, 'user/mypage.html')
    

# 비밀번호 변경
@login_required
def pw_change(request):
    if request.method == 'POST':
        pw1 = request.POST.get('password1', None)
        pw2 = request.POST.get('password2', None)
        if pw1 != pw2:
            return render(request, 'user/pwchange.html', {'error': '비밀번호가 일치하지 않습니다.'})
        user = request.user
        user.set_password(pw2)
        user.save()
        auth.logout(request)
        return redirect('/')

    else:
        if request.user.login_method != 'email':
            return redirect('/user/mypage')
        return render(request, 'user/pwchange.html')


certify_num = ''

# 이메일 인증번호 보내기
def email_ajax(request):
    global certify_num
    if request.method == 'POST':
        print('hi')
        certify_num = randint(10000, 99999)

        email = json.loads(request.body)
        print(email)
        send_mail('알song달song 회원가입 인증 메일입니다.',
                  f'아래의 인증번호를 입력해주세요🔐✨\n\n인증번호 : {certify_num}', 'jibeenpark@gmail.com', [email],
                  fail_silently=False)
        context = {
            'result': '인증번호 발송이 완료되었습니다.',
        }

    return JsonResponse(context)

# 인증번호 확인
def certify_ajax(request):
    global certify
    if request.method == 'POST':
        num = json.loads(request.body)
        result_msg = ''
        if num == str(certify_num):
            result_msg = '인증번호가 일치합니다.'
            certify = True
        else:
            result_msg = '인증번호가 다릅니다.'

        context = {
            'result': result_msg,
        }
    return JsonResponse(context)


# 임시 비밀번호 발급(아이디는 알고 비밀번호 모를 때)
def is_id(request):
    data = json.loads(request.body)
    try:
        # 아이디 유무 확인
        user = get_user_model().objects.get(username=data)
        # 카카오로 회원가입 한 경우 안 됨
        if user.login_method != 'email':
            context = {'result': '카카오로 로그인해주세요.', 'sns': 'sns'}
            return JsonResponse(context)
        email = user.email
        # 임시 비밀번호 생성
        temp_pw = ''
        for _ in range(15):
            temp_pw += str(random.choice(string.ascii_lowercase + string.digits))
        user.set_password(temp_pw)
        user.save()
        # 임시 비밀번호 발송
        send_mail('알song달sont 임시 비밀번호 메일입니다.',
                  f'아래의 임시 비밀번호를 사용하여 로그인 해주세요.\n로그인 후 반드시 비밀번호를 변경 해주세요.\n\n임시 비밀번호 : {temp_pw}',
                  'jibeenpark@gmail.com', [email], fail_silently=False)
        context = {
            'result': '등록된 이메일로 임시 비밀번호가 발송되었습니다.', 'ok': 'ok'
        }
        return JsonResponse(context)
    except:
        context = {'result': '등록된 아이디가 존재하지 않습니다.'}

    return JsonResponse(context)


# 프로필사진 변경 --> DB 연결 후 가능
def my_modify(request):
    if request.method == 'POST':
        img_file = request.FILES['file']
        ex = img_file.name.split('.')[-1]
        user = request.user
        url = 'https://retroflix.s3.ap-northeast-2.amazonaws.com/profile_img/' # 우리 DB로 바꿔야 함
        img_file.name = 'image-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.' + ex
        user.profile_img = img_file
        user.save()
        user.profile_img = url + str(img_file)
        user.save()
    return redirect('/user/mypage')
