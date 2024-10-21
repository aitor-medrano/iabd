from datasets import load_dataset

# Cargando train y test
ficheros_datos = {"train": "train-v2.0-es.json", "test": "dev-v2.0-es.json"}
squad_dataset_traintest = load_dataset("json", data_files=ficheros_datos, field="data")

squad_train = squad_dataset_traintest["train"]
print(squad_train[0]["title"]) # Beyoncé Knowles
squad_train_shuffled = squad_train.shuffle(seed=333)
print(squad_train_shuffled[0]["title"]) # Carnaval

# Seleccionamos X filas
tres_filas = squad_train_shuffled.select([5,10,15])
print(tres_filas)
seis_filas = squad_train_shuffled.select(range(6))
print(seis_filas)

# Filtramos las filas que empiezan por b
empieza_por_b_filas = squad_train_shuffled.filter(lambda x: x["title"].startswith("B"))
for i in range(empieza_por_b_filas.num_rows):
    print(empieza_por_b_filas[i]["title"])

# Añadimos una nueva columna
nueva_columna = ["nueva"] * squad_train_shuffled.num_rows
squad_train_shuffled = squad_train_shuffled.add_column(name="inicial",column=nueva_columna)
print(squad_train_shuffled)

# Le cambiamos el nombre
squad_train_shuffled = squad_train_shuffled.rename_column(
    original_column_name="inicial", new_column_name="modificada"
)
print(squad_train_shuffled)

squad_train_shuffled = squad_train_shuffled.remove_columns("modificada")
print(squad_train_shuffled.features)

squad_train_shuffled = squad_train_shuffled.flatten()
print(squad_train_shuffled)