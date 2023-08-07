<div align="center">

![알송달송_logo](https://velog.velcdn.com/images/doodjb/post/73061706-ada4-486f-bcbe-fc83f79455a6/image.png)

**“ _뭐 부를지 고민될 땐❓ 알송달송 해 ❗_ ”**

<br>
<br>

**`알송달송`** 은 **이원화된 노래방 곡 데이터를 한 데 모아 검색 및 저장**하고, <br>
**저장된 곡을 기반으로 어울리는 부를 곡 추천**을 받을 수 있는 **`노래방 곡정보 저장 & 추천 모바일 웹 서비스`** 입니다. <br>
<br>
( :iphone: 모바일 환경에서 접속할 것을 권장합니다 )



<br>

---
<br>

### 🤔 저번에 뭐 부르려고 했더라..? 새로 부를 거 없나..?

<br>

자주 부르는 애창곡을 **노래방 곡번호와 함께 저장 해두고 싶은 사람들**,

늘 부르던 노래가 지겨워져 **새로운 곡을 추천받고 싶지만 내게 어울릴까 고민인 사람들**!

**`알송달송`** 은 이러한 분들을 위해 만들어졌습니다.

</div>

<br>
<br>

## 🎤 화면 구성도
![알송달송_UI_1](https://velog.velcdn.com/images/doodjb/post/6f4b07f5-e024-482d-9bb4-9b6c12dfd635/image.PNG)
![알송달송_UI_2](https://velog.velcdn.com/images/doodjb/post/e69e2de1-143e-4975-8835-4679859a9e90/image.PNG)

[📽️ **UI 프로토타입 확인하기**](https://www.figma.com/proto/4SBwiDACv8g30oe4ifpTBE/%EC%95%8C%EC%86%A1%EB%8B%AC%EC%86%A1-%EC%99%84%EC%84%B1%EB%B3%B8?embed_host=notion&kind=&node-id=2-684&page-id=0:1&scaling=scale-down&starting-point-node-id=2:684&t=Kd6YvAvIhqwzJLHu-1&mode=design)
<br>
<br>
## 🎤 주요 기능

### 📥 *노래방에서 부를 곡 >저장< 기능*

	폴더 생성 👉🏻 곡 검색 or 인기차트를 통해 원하는 곡 선택
	👉🏻 저장할 폴더 지정 👉🏻 저장
<br>

### 🤖 *노래방에서 부를 곡 >추천< 기능*

-   **추천 페이지를 통해 추천 받기**
    
	    알송Ai 페이지 접속 👉🏻 추천 받기 원하는 폴더 선택 👉🏻 추천 결과 확인
    
-   **폴더 상세 페이지에서 추천 받기**
    
	    폴더 상세 페이지 접속 👉🏻 하단의 추천 섹션을 통해 알송Ai 페이지 접속 
	    👉🏻 (이하 로직은 위의 '추천 페이지를 통해 추천 받기'와 동일)
<br>

**∴ 추천 모델 최초 1회 실행 이후 폴더 상세 페이지 내에서 추천곡 3곡 간단히 확인 가능**

<br>
<br>

### 세부 워크플로우

<details>
<summary>🔎열어보기</summary>
<div markdown="1">

<br>

<details>
<summary>📄메인 페이지</summary>
<div markdown="1">

	-   네비게이션바 (홈, 검색, 인기차트, 알송Ai, 내 정보)
	-   곡 검색 페이지 유도 버튼
	-   약식 유저 대시보드
	-   Ai 곡 추천 페이지 유도 버튼
	-   부를 곡 폴더 추가 기능

</div>
</details>

<details>
<summary>📄내 폴더 페이지</summary>
<div markdown="1">

	-   폴더 삭제
	-   폴더명 변경
	-   곡 선택
	-   선택 곡 삭제
	-   추천 곡 제안
	-   추천 곡 더보기
	-   추천 곡 지금 폴더에 추가

</div>
</details>

<details>
<summary>📄곡 검색 페이지</summary>
<div markdown="1">

	-   제목/가수 선택
	-   검색창
	-   곡 검색 결과

</div>
</details>

<details>
<summary>📄인기 차트 페이지</summary>
<div markdown="1">

	-   TJ/KY 선택 기능
	-   TOP100 인기차트
	-   선택 곡 담기 기능

</div>
</details>

<details>
<summary>📄Ai 곡 추천 페이지</summary>
<div markdown="1">

	-   모델 실행 버튼
	-   모델 추천 결과 확인(10곡)

</div>
</details>

<details>
<summary>📄마이 페이지</summary>
<div markdown="1">

	-   프로필 이미지
	-   비밀번호 변경
	-   문의하기
	-   로그아웃
	-   도움말 배너

</div>
</details>

<br>

<details>
<summary>🔒 로그인 페이지</summary>
<div markdown="1">

	-   아이디
	-   비밀번호
	-   회원가입(일반)
	-   소셜로그인(kakao 로그인)
	-   비밀번호 찾기

</div>
</details>

<details>
<summary>🔑 회원가입 페이지</summary>
<div markdown="1">

	-   이메일
	-   아이디
	-   비밀번호
	-   비밀번호 확인
	-   닉네임
	-   이메일
	-   생년월일
	-   성별
	-   로그인 페이지로

</div>
</details>

</div>
</details>

<br>
<br>

## 🎤 DB ERD

<details>
<summary>🔎열어보기</summary>
<div markdown="1">

![DB ERD](https://velog.velcdn.com/images/doodjb/post/a53bf08d-8745-4c30-9b71-b349b33da6bc/image.png)

</div>
</details>

<br>
<br>

## 🎤 DFD

<details>
<summary>🔎열어보기</summary>
<div markdown="1">
  
(추가 예정)

</div>
</details>

<br>
<br>

## 🎤 사용 기술 스택

<details>
<summary>🔎열어보기</summary>
<div markdown="1">

| ⚙️ 기술 스택 | 👇🏻 사용 목적 |
|--|--|
| **`django`** | 알송달송 웹 서비스 구현 |
| **`fastapi`** | 추천 모델 serving |
| **`word2vec`** | 곡 추천 model 학습 |
| **`AWS(bucket)`** | 학습된 모델 파일 적재 |
| **`airflow`** | 노래방 곡정보/인기차트 ETL 과정 자동화 |
| **`celery`**, **`rabbitmq`**, **`redis`** | 트래픽 분산, 로그 적재 |
| **`postgreDB`**, **`mongoDB`** | 데이터베이스 활용 |
| **`nginx`**, **`gunicorn`** | Web서버와 WAS 분리 |
| **`GCP(Google Cloud Platform)`** | 배포를 위한 클라우드 서비스 활용 |
| **`docker`**, **`docker compose`** | 배포를 위한 작업 환경 도커라이징 |
| **`elastic search`**, **`logstash`**, **`kibana`** | 검색 기능 고도화, 데이터 시각화 |
| **`OpenAI`** | ChatGPT를 활용해 추천 결과 예외 후처리 |
| **`kakaoAPI`** | 소셜 로그인 구현 |

</div>
</details>

<br>
<br>

## 🎤 팀원 정보
> **이름(+깃허브링크)**,  **사진**,  **팀 내 Role**,  **담당 기술 스택** 순
<br>

| [박지빈](https://github.com/JIBEEN) | 오준 | 이정연 | 장진혁 | 장희수 | 정기원 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| ![Jibeen](https://velog.velcdn.com/images/doodjb/post/26d74b51-7df9-4d58-9ff6-19781f89b15f/image.jpg) | ![Oh](https://velog.velcdn.com/images/doodjb/post/62f8d3d0-39b1-47b8-b248-984dba43267e/image.png) | ![happyyeon](http://k.kakaocdn.net/dn/igE6M/btsjnIGUOeO/hGFgMxZFmO5ueibtEKBtu0/img_640x640.jpg) | ![Jinhuck](https://velog.velcdn.com/images/doodjb/post/5457db0d-86d3-4557-a841-8fc2bb19a9d8/image.png) | ![tbtgmltn97](https://velog.velcdn.com/images/doodjb/post/3cdab865-43c7-4e46-8475-881913760507/image.png) | ![kiwon](http://k.kakaocdn.net/dn/hFPGA/btspl7OFABY/z9eM8PVAiHb6X8D8OTlsZk/img_640x640.jpg) |
| `배포`, <br>`Data Engineering`,<br>`Back-end`,<br>`UI디자인` | `Data Engineering`,<br>`ML Engineering` | `배포` | `Back-end`,<br>`Front-end` | `Data Engineering`,<br>`ML Engineering` | `Data Engineering` |
| **`Docker`**, **`django`**,<br> **`GCP`**, **`Figma`**, **`Nginx`**, <br>**`Gunicorn`**, **`Airflow`** | **`FastAPI`**, **`Airflow`**,<br> **`CELERY`**, **`RabbitMQ`**,<br> **`Redis`**, **`GCP`**,<br> **`Docker`**, **`MongoDB`** | **`Docker`**,<br> **`AWS`**, **`Nginx`**,<br> **`Gunicorn`** | **`django`**,<br> **`elastic search`** | **`Airflow`**, **`PostgresDB`**,<br> **`MongoDB`**, **`Redis`**,<br> **`RabbitMQ`**, **`Docker`** | **`elastic search`**,<br> **`GCP`** |
<br>
<br>

## ⚖️ Rule

-   코드 작성은 **스네이크 표기법**을 따른다.
    
-   파일/디렉토리 이름은 전부 소문자로 작성하되 최대한 **직관적인 한 단어**로 명명한다.
    
-   2개의 단어 이상을 조합할 때는 **하이픈(-)을 사용**한다.
    
    ex) play-data
    
-   함수의 시작은 **동사형**으로
    
-   코드는 가독성을 우선시 한다. **comprehension 사용 자제**
    

