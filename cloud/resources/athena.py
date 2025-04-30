import boto3
import time

def ejecutar_consulta_athena(consulta, basededatos, destino_salida):
    response = cliente_athena.start_query_execution(
        QueryString=consulta,
        QueryExecutionContext={ 'Database': basededatos },
        ResultConfiguration={ 'OutputLocation': destino_salida }
    )
    return response['QueryExecutionId']

def obtener_estado(query_execution_id):
    response = cliente_athena.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    return response['QueryExecution']['Status']['State']

def obtener_resultado(query_execution_id):
    response = cliente_athena.get_query_results(
        QueryExecutionId=query_execution_id
    )
    # Process and print/query the results
    for fila in response['ResultSet']['Rows']:
        print([campo['VarCharValue'] for campo in fila['Data']])

cliente_athena = boto3.client('athena')

sql = "SELECT custid, fname, lname FROM customers_parquet WHERE city='Caguas' LIMIT 10;"
bd = "s8a_retail"
destino = "s3://s3severo8a-cli/athena-results/"

query_execution_id = ejecutar_consulta_athena(sql, bd, destino)
while obtener_estado(query_execution_id) == 'RUNNING' or obtener_estado(query_execution_id) == 'QUEUED':
    print("La consulta se está ejecutando...")
    time.sleep(3)  # Esperamos unos segundos

if obtener_estado(query_execution_id) == 'SUCCEEDED':
    print("!Consulta exitosa!")
    obtener_resultado(query_execution_id)
else:
    print("La consulta falló o ha sido cancelada", obtener_estado(query_execution_id))