# (가제)알song달song🎤✨

## 🗺️ Project Architecture
> 전체 프로젝트 구성에 대한 아키텍처 입니다   
![1  project_architecture](https://github.com/sexyzun/ddip/assets/42824372/8d15fde9-fb58-4dcd-ad48-4e52aa5dd0f7)
 

## 🗺️ Web Architecture
> 웹 배포에 대한 아키텍처 입니다   
![2  web_architecture](https://github.com/sexyzun/ddip/assets/42824372/95e2e1c8-6b4f-4574-b4fb-495ad6fff240)
 

## 🗺️ Django Architecture
> Django로 구현되는 애플리케이션 구조에 대한 아키텍처 입니다   
![3  django_architecture](https://github.com/sexyzun/ddip/assets/42824372/90e1bb70-4908-404e-9312-9acba04fc175)

### Django API Speicification

> 1️⃣ 회원 API
> 
>   |  HTTP |  Path |  Method |  Permission |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**POST** |/api/user/signup|CREATE| AllowAny |사용자 회원가입|
>   |**POST** |/api/user/signin|NONE| AllowAny |사용자 로그인, access_token 생성 및 반환|
>   |**API** |/api/user/login/kakao/|NONE| AllowAny |카카오 소셜 로그인, access_token 생성 및 반환|
>   |**API** |/api/user/login/naver/|NONE| AllowAny |네이버 소셜 로그인, access_token 생성 및 반환|    
> 
> 
> 2️⃣ 싱잉 리스트 API
> 
>   |  HTTP |  Path |  Method |  Permission |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/api/songs/|LIST| AllowAny |모든 곡  목록 확인|
>   |**GET**, **PUT**, **DELETE** |/api/songs/<int:pk>/|RETRIEVE, DESTORY| Access_token or ReadOnly OR IsOwner |곡 하나 확인, 삭제|
>   |**POST** |/api/songs/add/|CREATE| Access_token |곡 추가|
>
>
> 3️⃣ 게시판 API
> 
>   |  HTTP |  Path |  Method |  Permission |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/api/posts/|LIST| AllowAny |모든 게시글 목록 확인|
>   |**GET**, **PUT**, **DELETE** |/api/posts/<int:pk>/|RETRIEVE, UPDATE, DESTORY| Access_token or ReadOnly OR IsOwner |게시글 하나 확인, 수정, 삭제|
>   |**POST** |/api/posts/create/|CREATE| Access_token |게시글 생성|
>   |**POST** |/api/posts/<int:pk>/comments/create|CREATE| Access_token | 해당 게시글에 댓글 생성|
>   |**GET**, **PUT**, **DELETE**|/api/posts/<int:pk>/comments/|RETRIEVE, UPDATE, DESTORY| Access_token |댓글 확인, 수정, 삭제|
>   |**GET**|/api/posts/search/category/|LIST|AllowAny|카테고리별 검색|

## 🗺️ ML Architecture
> 추천시스템 머신러닝 구조에 대한 아키텍처 입니다   
![4  ML_architecture](https://github.com/sexyzun/ddip/assets/42824372/8b70f957-840a-454d-bfdd-1f4bc4de97fd)
 

## 🗺️ Layer Architecture
> 서비스 레이어에 따른 아키텍처 입니다   
![5  layer_architecture](https://github.com/sexyzun/ddip/assets/42824372/3a948f97-1b85-438b-8c40-6e66d4f2caef)

## Schedule

- 1주차: 시스템 아키텍처 설계 및 멘토 선정
- 2주차~5주차: 장고 개발(로컬 환경) / 추천시스템 모델 병행 제작
- 6주차: 장고 + 추천시스템 병합 (로컬 환경) / 추천시스템 모델 성능 평가(모의 테스터 모집)
- 7주차: 코드 리팩토링
- 8주차: AWS 배포
- 9주차: AWS 배포
- 10주차: PT 제작 및 발표 준비

## ⚖️ Rule

**2023 Play Data - Data Engineering 22nd**   

- 코드 작성은 스네이크 표기법을 따른다.
- 파일/디렉토리 이름은 전부 소문자로 작성하되 최대한 직관적인 한 단어로 명명한다.
- 2개의 단어 이상을 조합할 때는 하이픈(-)을 사용한다.
- Ex) play-data
- 함수의 시작은 동사형으로
- 코드는 가독성을 우선시 한다. comprehension 사용 자제
