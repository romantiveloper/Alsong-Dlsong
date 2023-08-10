import redis
from pymongo import MongoClient
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow import DAG
from datetime import datetime, timedelta
import airflow.utils.dates
import json

secrets_path = '/etc/airflow/secrets.json'

with open(secrets_path) as f:
    secrets = json.loads(f.read())


def _redis_to_mongo():
    # Redis 연결
    r = redis.StrictRedis(host=secrets['redis_ADDRESS']['host'], port=secrets['redis_ADDRESS']['port'], db=secrets['redis_ADDRESS']['db'], password=secrets['redis_ADDRESS']['password'])
    # MongoDB 연결
    client = MongoClient(secrets['mongo_ADDRESS'])
    db = client["my_db"]
    coll = db["my_collection"]


    # 어제 날짜 생성
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # 어제 날짜를 포함한 모든 키값 조회
    keys = r.keys(f"*{yesterday}*")
    data = []
    for key in keys:
        utf8_key = key.decode('utf-8')
        utf8_value = r.get(key).decode('utf-8')

        try:
            # value를 정수로 변환하여 저장할 수 있으면 리스트 타입으로 저장
            values = [str(val) for val in utf8_value.split(',')]
        except ValueError:
            # value가 정수가 아니면 문자열로 저장
            values = utf8_value.split(',')

        temp = {'key': utf8_key, 'value': values}
        data.append(temp)

    # 데이터가 있는 경우 MongoDB에 적재
    if len(data) > 0:
        try:
            coll.insert_many(data)
        except Exception as e:
            print(f"An error occurred while inserting data into MongoDB: {str(e)}")

with DAG(
dag_id='redis_to_mongo',
start_date=airflow.utils.dates.days_ago(1),
schedule_interval= '0 7 * * *',
) as dag:

    start = DummyOperator(task_id='start')
    redis_to_mongo = PythonOperator(
        task_id="redis_to_mongo",
        python_callable=_redis_to_mongo)
    start >> redis_to_mongo
                                                            