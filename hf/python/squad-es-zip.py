from datasets import load_dataset

ficheros_datos = {"train": "train-v2.0-es.json.zip", "test": "dev-v2.0-es.json.zip"}
squad_dataset_traintest = load_dataset("json", data_files=ficheros_datos, field="data")
print(squad_dataset_traintest)