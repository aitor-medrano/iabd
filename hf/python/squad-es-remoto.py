from datasets import load_dataset

url = "https://raw.githubusercontent.com/ccasimiro88/TranslateAlignRetrieve/master/SQuAD-es-v2.0/"

ficheros_datos = {
    "train": url + "train-v2.0-es.json",
    "test": url + "dev-v2.0-es.json",
}
squad_remote_dataset = load_dataset("json", data_files=ficheros_datos, field="data")

print(squad_remote_dataset)