"""Informe para negocio: se ejecuta cada vez que retail_elt publica los marts."""
import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import Asset, dag
 
MARTS = Asset("s3://processed/marts/ingresos_por_departamento.parquet")
  
@dag(
    schedule=[MARTS],
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    tags=["iabd", "elt"],
)
def informe_departamentos():
    BashOperator(
        task_id="informar",
        bash_command="$ELT_BIN/python /workspace/pipeline/informe.py",
    )
 
informe_departamentos()