from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,  # 재시도 횟수
    'retry_delay': timedelta(minutes=2),  # 재시도 간격
}



dag = DAG(
    dag_id='run_model_on_remote_container',
    default_args=default_args,
    description='Run model.py on k-ict container',
    schedule_interval='0 0 15 * *',     # 매월 15일 자정
    catchup=False
)

wait_for_data_update = ExternalTaskSensor(
    task_id='wait_for_data_update',
    external_dag_id='final',  # DAG 1의 이름을 여기에 명시합니다.
    external_task_id='load_add_new_song_master',  # DAG 1의 최종 태스크의 이름을 여기에 명시합니다.
    allowed_states=['success'],  # 실행이 허용되는 상태 목록입니다.
    check_existence=True,  # 대기 중인 DAG/예약된 태스크가 존재하는지 여부를 검사합니다.
    dag=dag
)


run_model_on_container = SSHOperator(
    task_id='run_model_on_container',
    ssh_conn_id='k-ict_ssh',
    command='/opt/conda/bin/python /root/data/sing_list/song2vec.py',
    cmd_timeout=30.0 * 60,  # 초 단위로 표현한 30분 (30 * 60초)
    dag=dag,
    wait_for_downstream=True  # 이전 DAG의 모든 태스크가 완료될 때까지 기다리도록 설정합니다.
)

wait_for_data_update >> run_model_on_container