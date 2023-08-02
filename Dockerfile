FROM ubuntu:22.04

# 우분투에서 다운로드 속도가 느리기 때문에 다운로드 서버를 바꿔주었다
RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list

# apt 업그레이트 및 업데이트
RUN apt-get -y update && apt-get -y dist-upgrade

# apt-utils dialog : 우분투 초기 설정 / libpq-dev : PostgreSQL 의존성
RUN apt-get install -y apt-utils dialog libpq-dev

# pip dev 설치
RUN apt-get install -y python3-pip python3-dev

# 파이썬에서 콘솔 출력이 느릴 경우 다음과 같이 환경 변수를 설정해준다.
ENV PYTHONUNBUFFERED=0

# Django 기본 언어를 한국어로 설정하면 파이썬 기본 인코딩과 충돌되어 한글 출력, 입력시에 에러가 난다.
# 따라서 파이썬 기본 인코딩을 한국어를 사용할 수 있는 utf-8으로 설정한다.
ENV PYTHONIOENCODING=utf-8

RUN mkdir /config

# 호스트에 있는 requirements.txt 파일을 컨테이너 내부로 복사해준다.
ADD /config/requirements.txt /config/

# requirements.txt에 있는 파이썬 패키지 설치
RUN pip3 install -r /config/requirements.txt

### 작업 디렉토리 ###
# Django 소스코드가 들어갈 폴더 생성
RUN mkdir /src;

# 작업 디렉토리 src로 변경
WORKDIR /src

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
