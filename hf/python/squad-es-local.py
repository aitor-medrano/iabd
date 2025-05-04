from datasets import load_dataset

squad_dataset = load_dataset("json", data_files="train-v2.0-es.json", field="data")

print(squad_dataset)
print(squad_dataset["train"].features)

# Visualizando el contenido
print(squad_dataset["train"][0]["title"])
print(squad_dataset["train"][0]["paragraphs"][0])

# Cargando train y test
ficheros_datos = {"train": "train-v2.0-es.json", "test": "dev-v2.0-es.json"}
squad_dataset_traintest = load_dataset("json", data_files=ficheros_datos, field="data")
print(squad_dataset_traintest)
