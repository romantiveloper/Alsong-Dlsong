## 😎airflow를 compose 형태로 묶음😎

### 1) 신곡 수집 자동화
  > 🎤TJ, KY 노래 데이터 수집 -> 🛠️전처리 -> 🐘postgresql DB 적재

      1-1. 하루 간격으로 수집되는 신곡 업데이트! 
      1-2. TJ와 KY를 최대한 잘 합치기 위한 데이터 전처리 과정 
      1-3. 중복을 제거하여 DB 적재
   
### 2) 인기차트 수집 자동화
> 🎤TJ, KY TOP 100 인기차트 데이터 수집 -> 🐘postgresql DB 적재

      2-1. 일주일 간격으로 최신화되는 인기차트

### 3) 로그 데이터 적재 (redis -> mongoDB) 자동화
> ❓❗AlsongDlsong🎶 실제 User들이 추천을 클릭✅ -> redis에 User의 플레이리스트🎤 저장 -> 🍃mongoDB에 적재

      3-1. 하루 간격으로 로그 적재 (redis -> mongo)  
      3-2. 해당 날짜 기준 어제 적재된 값들만 mongoDB로 적재

### 4) 모델 재학습 자동화
> mongoDB에 저장된 값 -> gpu container -> model 재학습

      4-1. 하루 간격으로 모델 업데이트
      4-2. Airflow에 SSH connector 등록 후 통신
