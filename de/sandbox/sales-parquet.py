import pandas as pd
import math

# Leemos el csv mediante pandas
df = pd.read_csv('pdi_sales.csv', sep=';')

# Limpiamos los datos (strip a los códigos postales)
df['Zip'] = df['Zip'].str.strip()
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y') 

# Ordenamos por pais
df = df.sort_values(by=['Country', 'Date', 'ProductID', 'Zip'])

# Calculamos cuántas filas debe tener cada grupo para que salgan exactamente 4
total_filas = len(df)
filas_por_grupo = math.ceil(total_filas / 4)

# Guardamos directamente a Parquet (sin esquema explícito)
df.to_parquet(
    'pdi_sales.parquet', 
    engine='pyarrow', 
    index=False,
    row_group_size=filas_por_grupo
)