from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook

from datetime import datetime
from datetime import timedelta
# from plugins import slack

import requests
import logging
import psycopg2



def get_Redshift_connection(autocommit=False):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()

def create_temp_table(schema, table, temp_table):
    sql = f"DROP TABLE IF EXISTS {schema}.{temp_table};"
    sql += f"CREATE TABLE {schema}.{temp_table} AS SELECT * FROM {schema}.{table};"
    return sql

def upsert(schema, table, temp_table, data):
    sql = ""
    for d in data:
        sql += f"""INSERT INTO {schema}.{temp_table} VALUES ('{d[0]}', '{d[1]}', '{d[2]}', '{d[3]}', '{datetime.now()}');"""
    sql += f"BEGIN; DELETE FROM {schema}.{table};"

    sql += f"""INSERT INTO {schema}.{table} \
    SELECT date, temp, min_temp, max_temp, created_date \
    FROM ( \
    SELECT *, ROW_NUMBER() OVER(PARTITION BY date ORDER BY created_date DESC) seq \
    FROM {schema}.{temp_table}) \
    WHERE seq=1;
     """
     
    sql += "END;"
    return sql


def extract(**context):
    link = context["params"]["url"]
    coordinate = context["params"]["coordinate"]
    key = context["params"]["key"]

    execution_date = context['execution_date']
    logging.info(execution_date)

    r = requests.get(f"{link}?lat={coordinate['lat']}&lon={coordinate['lon']}&appid={key}&units=metric")
    return (r.json())


def transform(**context):
    r_json = context["task_instance"].xcom_pull(key="return_value", task_ids="extract")
    
    data = []
    for d in r_json["daily"]:
        data.append([
            datetime.fromtimestamp(d["dt"]).strftime('%Y-%m-%d'),
            d["temp"]["day"],
            d["temp"]["min"],
            d["temp"]["max"]
            ])
    return data


def load(**context):
    schema = context["params"]["schema"]
    table = context["params"]["table"]
    temp_table = context["params"]["temp_table"]
    
    cur = get_Redshift_connection(True)
    data = context["task_instance"].xcom_pull(key="return_value", task_ids="transform")
    
    cur.execute(create_temp_table(schema, table, temp_table))

    try:
        cur.execute(upsert(schema, table, temp_table, data))
    except (Exception, psycopg2.DatabaseError) as error:
        cur.execute("ROLLBACK;")
        print(error)
        raise


dag = DAG(
    dag_id = 'incremental_update',
    start_date = datetime(2023,4,6), # 날짜가 미래인 경우 실행이 안됨
    schedule = '0 2 * * *',  # 적당히 조절
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
        # 'on_failure_callback': slack.on_failure_callback,
    }
)


extract = PythonOperator(
    task_id = 'extract',
    python_callable = extract,
    params = {
        'url': Variable.get("weather_url"),
        'coordinate': Variable.get("gps_coordinates", deserialize_json=True)["Asia/Seoul"],
        'key': Variable.get("api_key")
    },
    dag = dag)

transform = PythonOperator(
    task_id = 'transform',
    python_callable = transform,
    params = { 
    },  
    dag = dag)

load = PythonOperator(
    task_id = 'load',
    python_callable = load,
    params = {
        'schema': 'skh951225',
        'table': 'weather_forecast',
        'temp_table': 'temp_weather_forecast'
    },
    dag = dag)

extract >> transform >> load

