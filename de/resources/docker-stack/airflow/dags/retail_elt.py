from datetime import timedelta
 
import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import CronTriggerTimetable, dag
 
PROYECTO = "/workspace/dbt/iabd" # define la ruta del proyecto dbt, que es donde se ejecutará dbt run y dbt test
 
@dag(
    schedule=CronTriggerTimetable("0 6 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(seconds=30),
        "pool": "duckdb",
    },
    tags=["iabd", "elt"],
)
def retail_elt():
    extraer = BashOperator(
        task_id="extraer",
        bash_command="$ELT_BIN/python /workspace/dlt/retail_el.py",
    )
 
    transformar = BashOperator(
        task_id="transformar",
        bash_command="$ELT_BIN/dbt run --profiles-dir .",
        cwd=PROYECTO,
    )
 
    probar = BashOperator(
        task_id="probar",
        bash_command="$ELT_BIN/dbt test --profiles-dir .",
        cwd=PROYECTO,
        retries=0,  # con los mismos datos, una prueba que falla vuelve a fallar
    )
 
    extraer >> transformar >> probar
 
 
retail_elt()