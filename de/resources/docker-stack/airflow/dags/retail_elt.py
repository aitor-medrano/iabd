from datetime import timedelta
 
import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import CronTriggerTimetable, dag
 
# Proyecto dbt de la sesión de transformación: dbt se ejecuta desde aquí
PROYECTO = "/workspace/dbt/iabd_retail"
PERFIL = "/workspace/dbt/iabd"
 
@dag(
    schedule=CronTriggerTimetable("0 6 * * *", timezone="UTC"),         # (1)!
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,                                                  # (2)!
    default_args={                                                      # (3)!
        "retries": 1,
        "retry_delay": timedelta(seconds=30),
        "pool": "duckdb",
    },
    tags=["iabd", "elt"],
)
def retail_elt():
    extraer = BashOperator(
        task_id="extraer",
        bash_command="$ELT_BIN/python /workspace/dlt/retail_el.py",    # (4)!
    )
 
    transformar = BashOperator(
        task_id="transformar",
        bash_command=f"$ELT_BIN/dbt run --profiles-dir {PERFIL}",
        cwd=PROYECTO,                                                  # (5)!
    )
 
    probar = BashOperator(
        task_id="probar",
        bash_command=f"$ELT_BIN/dbt test --profiles-dir {PERFIL}",
        cwd=PROYECTO,
        retries=0,  # con los mismos datos, una prueba que falla vuelve a fallar
    )
    
    publicar = BashOperator(
        task_id="publicar",
        bash_command="$ELT_BIN/python /workspace/pipeline/publicar.py",
    )
 
    extraer >> transformar >> probar >> publicar
 
 
retail_elt()