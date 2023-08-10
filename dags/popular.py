from datetime import datetime
import requests
import pandas as pd
import airflow.utils.dates
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from bs4 import BeautifulSoup as BS
from sqlalchemy import create_engine
import json

secrets_path = '/etc/airflow/secrets.json'

with open(secrets_path) as f:
    secrets = json.loads(f.read())

DB_ADDRESS = secrets['DB_ADDRESS']

# 적재할 DB 설정
engine = create_engine(secrets['DB_ADDRESS'])


head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
# 연, 월 처리
# 월 형태 "0n"으로 변환
year = datetime.now().year
month = datetime.now().month
if month < 10 :
    month = '0' + str(month)
    
    
def _popular_tj():
    url_tj = f"https://www.tjmedia.com/tjsong/song_monthPopular.asp?strType=1&SYY={year}&SMM={month}&EYY={year}&EMM={month}"
    r = requests.get(url_tj,headers = head)
    r.encoding = 'utf-8'
    bs = BS(r.text)
    
    table = bs.find("table",class_="board_type1")
    
    new_pop_tj = pd.read_html(str(table))[0]
    new_pop_tj.rename(columns={'순위':'rank','가수':'artist','곡번호':'song_num_id','곡제목':'title'},inplace=True)
    new_pop_tj['id'] = new_pop_tj.index
    new_pop_tj.to_csv("/opt/airflow/data/jibeen_tj.csv",index=False)
    

def _popular_ky():
    ky_pop = []
    
    for page in range(1,3): # 1,2 페이지 모두 크롤링용
        url_ky = f"https://kysing.kr/popular/?period=&range={page}"
        r = requests.get(url_ky)
        
        # 해당 페이지의 인기곡 50곡 전체의 정보 크롤링
        ky_pop_chart = BS(r.text).find("form", {"id":"popular_chart_frm"}).findAll("ul", {"class":"popular_chart_list clear"})

        for song in ky_pop_chart[1:]: # 한 곡의 정보 set 불러옴, 헤드 행 제외 1번부터
            
            tmp_dict = {
                "rank" : song.find("span", {"class":"popular_chart_link"}).text, 
                "song_num_id" : song.find("li", {"class":"popular_chart_num"}).text, 
                "title" : song.find("span", {"class":"tit"}).text, 
                "artist" : song.find("span", {"class":"tit mo-art"}).text.replace(' ', ''), # 공백 제거
                # "출시일" : song.find("li", {"class":"popular_chart_rel"}).text 
            }
            
            ky_pop.append(tmp_dict)
        
        new_pop_ky = pd.DataFrame(ky_pop)
        new_pop_ky['id'] = new_pop_ky.index

        new_pop_ky.to_csv("/opt/airflow/data/jibeen_ky.csv",index=False)


def _load_postgresql():
    tj = pd.read_csv("/opt/airflow/data/jibeen_tj.csv")
    ky = pd.read_csv("/opt/airflow/data/jibeen_ky.csv")
    

    
    tj.to_sql(name='song_tj_pop', con=engine, if_exists='replace', index=False, method='multi', chunksize=1000)
    ky.to_sql(name='song_ky_pop', con=engine, if_exists='replace', index=False, method='multi', chunksize=1000)
    
    
with DAG(
    dag_id='top100',
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval='@monthly',
) as dag:
    
    start = DummyOperator(task_id='start')
    popular_tj = PythonOperator(
        task_id="popular_tj",
        python_callable=_popular_tj)
    popular_ky = PythonOperator(
        task_id="popular_ky",
        python_callable=_popular_ky)
    load_postgresql = PythonOperator(
        task_id="load_postgresql",
        python_callable=_load_postgresql)
    start >> [popular_tj, popular_ky] >> load_postgresql
