import re
from datetime import timedelta
import requests
import pandas as pd
import numpy as np
import json
import pathlib
import airflow.utils.dates
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from bs4 import BeautifulSoup as BS
import numpy as np
import psycopg2
from sqlalchemy import create_engine
import time
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


secrets_path = '/etc/airflow/secrets.json'

with open(secrets_path) as f:
    secrets = json.loads(f.read())
# 적재할 DB 설정
engine = create_engine(secrets['DB_ADDRESS'])
Session = sessionmaker(bind=engine)
session = Session()
result = session.execute(text(f"SELECT master_number FROM song_song ORDER BY master_number DESC LIMIT 1"))
last_master_number = result.fetchone()[0]
session.close()

# 전처리하는 함수
def _preprocess_sentence(sentence):
    
    # 단어와 구두점(punctuation) 사이의 거리를 만듭니다.
    # 예를 들어서 "I am a student." => "I am a student ."와 같이
    # student와 온점 사이에 거리를 만듭니다.
    
    sentence = re.sub(r'\[[^)]*\]', '', sentence)
    sentence = re.sub(r'\([^)]*\)', '', sentence)
    sentence = re.sub(r'★[^)]*★', '', sentence)
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    # (a-z, A-Z, ".", "?", "!", ",")를 제외한 모든 문자를 제거해준다.
    sentence = re.sub(r"[^a-zA-Zㄱ-ㅣ가-힣0-9?.!,]+", "", sentence)
    sentence = sentence.strip()
    sentence = sentence.lower()
    return sentence


# 플레이리스트의 (노래,가수) 정보를 매핑해주기 위해 (노래,가수) 형식으로 생성해주는 함수를 만들었고 'play'라는 새로운 컬럼으로 만들어준다.
def _combine_columns(x):
    return (x['master_title'], x['master_singer'])



head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
# tj에서 신곡 크롤링
def _new_tj():
    tj_url = "https://www.tjmedia.com/tjsong/song_monthNew.asp"
    r = requests.get(tj_url, headers = head)
    r.encoding = 'utf-8'
    bs = BS(r.text,features="lxml")
    table = bs.find("table",class_="board_type1")
    new_tj = pd.read_html(str(table))[0]
    new_tj = new_tj[['곡 번호','곡 제목','가수']]
    new_tj.rename(columns={'곡 번호':'tj_song_num_id','곡 제목':'title','가수':'artist'},inplace=True)
    new_tj['master_title'] = new_tj['title'].apply(lambda x : _preprocess_sentence(x))
    new_tj['master_singer'] = new_tj['artist'].apply(lambda x : _preprocess_sentence(x))
    new_tj['play'] = new_tj.apply(lambda x: _combine_columns(x), axis=1)
    new_tj['play'] = new_tj['play'].apply(lambda x : str(x))
    # new_tj['tj_song_num_id'] = new_tj['tj_song_num_id'].apply(lambda x : str(x))
    new_tj.to_csv("/opt/airflow/data/new_tj_after.csv", index = False)
    time.sleep(5)
    master_tj = pd.read_csv("/opt/airflow/data/master_tj.csv")
    time.sleep(5)
    add_tj = pd.merge(master_tj,new_tj,how='outer')
    add_tj.rename(columns={'tj_song_num_id':'song_num'},inplace=True)
    add_tj= add_tj.drop_duplicates(subset='song_num').reset_index(drop=True)
    add_tj.to_csv("/opt/airflow/data/add_tj.csv",index=False)
    time.sleep(5)

def _minus_tj():
    new_tj_before = pd.read_csv("/opt/airflow/data/new_tj.csv")
    time.sleep(5)
    new_tj_after = pd.read_csv("/opt/airflow/data/new_tj_after.csv")
    time.sleep(5)
    minus_tj = new_tj_after.merge(new_tj_before, how='outer', indicator=True)
    minus_tj = minus_tj[minus_tj['_merge'] == 'left_only'].drop('_merge',axis=1)
    minus_tj.to_csv("/opt/airflow/data/minus_tj.csv",index=False)
    time.sleep(5)
    new_tj_after.to_csv("/opt/airflow/data/new_tj.csv",index=False)
    time.sleep(5)

# tj신곡만 계속 업데이트가 되기 위해서는 우선 tj데이터가 song_tjsong에 있어야한다.
# tj신곡만 append
def _load_add_new_tj():
    minus_tj = pd.read_csv("/opt/airflow/data/minus_tj.csv")
    time.sleep(5)
    minus_tj = minus_tj.rename(columns={"tj_song_num_id":"song_num"})
    minus_tj.to_sql(name='song_tjsong', con=engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
# ky에서의 신곡 크롤링
def _new_ky():
    num = []
    title = []
    artist = []
    for page in range(1,50):
        try:
            url = f"https://kysing.kr/latest/?s_page={page}"
            r = requests.get(url, headers=head)
            bs = BS(r.text,features="lxml")
            for i in bs.findAll("li",class_="search_chart_num")[1:]:
                num.append(i.text)
            for i in bs.findAll("span",class_="tit")[::2]:
                title.append(i.text)
            for i in bs.findAll("li",class_="search_chart_sng")[1:]:
                artist.append(i.text)
        except:
            break
    new_ky = pd.DataFrame({'ky_song_num_id':num,'제목_KY':title,'가수_KY':artist})
    # 'master_title', 'master_singer'를 마스터 기준으로 만들어준다
    new_ky['master_title'] = new_ky['제목_KY'].apply(lambda x : _preprocess_sentence(x))
    new_ky['master_singer'] = new_ky['가수_KY'].apply(lambda x : _preprocess_sentence(x))
    new_ky['play'] = new_ky.apply(lambda x: _combine_columns(x), axis=1)
    new_ky['play']=new_ky['play'].apply(lambda x:str(x))
    new_ky['ky_song_num_id'] = new_ky['ky_song_num_id'].apply(lambda x : int(x))
    new_ky.to_csv("/opt/airflow/data/new_ky_after.csv",index=False)
    time.sleep(5)
    master_ky = pd.read_csv("/opt/airflow/data/master_ky.csv")
    time.sleep(5)
    master_ky['play']=master_ky['play'].apply(lambda x:str(x))
    add_ky = pd.merge(new_ky,master_ky,how='outer').reset_index(drop=True)
    add_ky.rename(columns={'ky_song_num_id':'song_num','제목_KY':'title','가수_KY':'artist'},inplace=True)
    add_ky= add_ky.drop_duplicates(subset='song_num').reset_index(drop=True)
    add_ky.to_csv("/opt/airflow/data/add_ky.csv",index=False)
    time.sleep(5)


def _minus_ky():
    new_ky_before = pd.read_csv("/opt/airflow/data/new_ky.csv")
    time.sleep(5)
    new_ky_after = pd.read_csv("/opt/airflow/data/new_ky_after.csv")
    time.sleep(5)
    minus_ky = new_ky_after.merge(new_ky_before, how='outer', indicator=True)
    minus_ky = minus_ky[minus_ky['_merge'] == 'left_only'].drop('_merge',axis=1)
    minus_ky.to_csv("/opt/airflow/data/minus_ky.csv",index=False)
    time.sleep(5)
    new_ky_after.to_csv("/opt/airflow/data/new_ky.csv",index=False)
    time.sleep(5)

# ky신곡만 계속 업데이트가 되기 위해서는 우선 ky데이터가 song_kysong에 있어야한다.
# ky신곡만 append
def _load_add_new_ky():
    minus_ky = pd.read_csv("/opt/airflow/data/minus_ky.csv")
    time.sleep(5)
    minus_ky = minus_ky.rename(columns={"ky_song_num_id":"song_num","제목_KY":"title","가수_KY":"artist"})
    minus_ky.to_sql(name='song_kysong', con=engine, if_exists='append', index=False, method='multi', chunksize=1000)  
    
    
def _new_song():
    new_tj = pd.read_csv("/opt/airflow/data/new_tj.csv")
    time.sleep(5)
    new_ky = pd.read_csv("/opt/airflow/data/new_ky.csv")
    time.sleep(5)
    new_song = pd.merge(new_tj,new_ky,how='outer')
    new_song.drop_duplicates(subset=['play'],keep='first',inplace=True)
    new_song.reset_index(drop=True, inplace=True)
    new_song['tj_song_num_id'] = pd.to_numeric(new_song['tj_song_num_id'], errors='coerce').fillna(0).astype(int)
    new_song['ky_song_num_id'] = pd.to_numeric(new_song['ky_song_num_id'], errors='coerce').fillna(0).astype(int)
    # new_song.fillna("?",inplace=True)
    # new_song['tj_song_num_id'] = new_song['tj_song_num_id'].apply(lambda x: int(x) if type(x) == float else x).apply(lambda x : str(x))
    # new_song['ky_song_num_id'] = new_song['ky_song_num_id'].apply(lambda x: int(x) if type(x) == float else x).apply(lambda x : str(x))
    new_song.to_csv("/opt/airflow/data/new_song.csv",index=False)
    time.sleep(5)


def _add_genre():
    new_song = pd.read_csv("/opt/airflow/data/new_song.csv")
    time.sleep(5)
    new_song['melon_tj'] = new_song['title'] + ' ' + new_song['artist']
    new_song['melon_ky'] = new_song['제목_KY'] + ' ' + new_song['가수_KY']
    for i in range(len(new_song)):
        if pd.isnull(new_song['melon_tj'][i]) and not pd.isnull(new_song['melon_ky'][i]):
            new_song['melon_tj'][i] = new_song['melon_ky'][i]
    new_song.drop(['melon_ky'],axis =1 ,inplace=True)
    melonid = []
    for keyword in new_song['melon_tj']:
        url = f"https://www.melon.com/search/song/index.htm?q={keyword}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T"
        r = requests.get(url,headers=head)
        time.sleep(1)
        bs = BS(r.text,features="lxml")
        button = bs.find("button", class_="btn_icon play")
        if button and button.has_attr("onclick"):
            onclick_value = button["onclick"]
            if onclick_value != 'NoneType':
                melonid_dict = {
                    'keyword': keyword,
                    'id': onclick_value.split(",")[-1].replace(");", "")
            }
        else:
            melonid_dict = {
                'keyword' : keyword,
                'id' : 'Null'
            }
        melonid.append(melonid_dict)
    df = pd.DataFrame(melonid)
    # 장르 크롤링하기
    tmp = []
    for i in df['id']:
        if i != 'Null':
            url = f"https://www.melon.com/song/detail.htm?songId={i}"
            r = requests.get(url, headers = head)
            bs = BS(r.text,features="lxml")
            tmp.append(bs.find("div").findAll("dd")[2].text)
        else:
            tmp.append(np.nan)
    new_song['genre']= tmp
    # new_song['genre'] = new_song['genre'].apply(lambda x : x.replace("Null","?"))
    # new_song.fillna("?",inplace=True)
    new_song.to_csv("/opt/airflow/data/new_song.csv",index=False)   
    time.sleep(5)
    
    
def _update_master():
    new_song = pd.read_csv("/opt/airflow/data/new_song.csv")
    new_song['genre'] = new_song['genre'].apply(lambda x : str(x))
    time.sleep(5)
    master = pd.read_csv("/opt/airflow/data/master.csv")
    time.sleep(5)
    master['tj_song_num_id'] = pd.to_numeric(master['tj_song_num_id'], errors='coerce').fillna(0).astype(int)
    master['ky_song_num_id'] = pd.to_numeric(master['ky_song_num_id'], errors='coerce').fillna(0).astype(int)
    master_after = pd.merge(new_song,master,how='outer')
    # master.fillna('?',inplace=True)
    master_after.drop_duplicates(subset='play',inplace=True)
    master.to_csv("/opt/airflow/data/master.csv",index=False)
    time.sleep(5)
    master_after.to_csv("/opt/airflow/data/master_after.csv",index=False)
    time.sleep(5)
    
def _minus_master():
    master_before = pd.read_csv("/opt/airflow/data/master.csv")
    time.sleep(5)
    master_after = pd.read_csv("/opt/airflow/data/master_after.csv")
    time.sleep(5)
    minus_master = master_after.merge(master_before, how='outer', indicator=True)
    minus_master = minus_master[minus_master['_merge'] == 'left_only'].drop('_merge',axis=1)
    minus_master.to_csv("/opt/airflow/data/minus_master.csv",index=False)
    time.sleep(5)
    master_after.to_csv("/opt/airflow/data/master.csv",index=False)
    time.sleep(5)
    
    
# 신곡만 계속 업데이트가 되기 위해서는 우선 master데이터(매칭데이터)가 song_song에 있어야한다.
def _load_add_new_song_master():
    add_tj = pd.read_csv("/opt/airflow/data/add_tj.csv")
    time.sleep(5)
    add_ky = pd.read_csv("/opt/airflow/data/add_ky.csv")
    time.sleep(5)
    minus_master = pd.read_csv("/opt/airflow/data/minus_master.csv")
    time.sleep(5)
    filtered_master_tj = minus_master[minus_master['tj_song_num_id'].isin(add_tj['song_num'])]
    filtered_master_ky = minus_master[minus_master['ky_song_num_id'].isin(add_ky['song_num'])]
    filtered_master = pd.concat([filtered_master_tj,filtered_master_ky])
    filtered_master.reset_index(drop=True,inplace=True)
    filtered_master['master_number']=filtered_master.index + (last_master_number + 1)
    filtered_master['cmp'] = np.nan
    filtered_master['writer'] = np.nan
    filtered_master.to_sql(name='song_song', con=engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
    


with DAG(
    dag_id='final',
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval='@daily',
) as dag:
    
    start = DummyOperator(task_id='start')
    new_tj = PythonOperator(
        task_id="new_tj",
        python_callable=_new_tj)
    minus_tj = PythonOperator(
        task_id="minus_tj",
        python_callable=_minus_tj)
    load_add_new_tj = PythonOperator(
        task_id="load_add_new_tj",
        python_callable=_load_add_new_tj)
    new_ky = PythonOperator(
        task_id="new_ky",
        python_callable=_new_ky)
    minus_ky = PythonOperator(
        task_id="minus_ky",
        python_callable=_minus_ky)
    load_add_new_ky = PythonOperator(
        task_id="load_add_new_ky",
        python_callable=_load_add_new_ky)
    new_song = PythonOperator(
        task_id="new_song",
        python_callable=_new_song)
    add_genre = PythonOperator(
        task_id="add_genre",
        python_callable=_add_genre)
    update_master = PythonOperator(
        task_id="update_master",
        python_callable=_update_master)
    minus_master = PythonOperator(
        task_id="minus_master",
        python_callable=_minus_master)
    load_add_new_song_master = PythonOperator(
        task_id="load_add_new_song_master",
        python_callable=_load_add_new_song_master)
    start >> new_tj >> minus_tj >> load_add_new_tj >> new_ky >> minus_ky >> load_add_new_ky >> new_song >> add_genre >> update_master >> minus_master >> load_add_new_song_master

