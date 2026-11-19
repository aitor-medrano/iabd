import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task
  
@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    catchup=False,
    tags=["iabd"],
)
def hola_airflow():
    saludar = BashOperator(
        task_id="saludar",
        bash_command="echo 'Hola desde Airflow. Fecha lógica: {{ ds }}'",
    )
 
    @task
    def resumir(ds=None, run_id=None):
        print(f"Ejecución {run_id} para el día {ds}")
 
    saludar >> resumir()
 
 
hola_airflow()