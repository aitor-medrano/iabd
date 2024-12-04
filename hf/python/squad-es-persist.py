from datasets import load_dataset

# Cargando train y test
ficheros_datos = {"train": "train-v2.0-es.json", "test": "dev-v2.0-es.json"}
squad_dataset = load_dataset("json", data_files=ficheros_datos, field="data")
print(squad_dataset.cache_files)
# {'train': [{'filename': '/Users/aitormedrano/.cache/huggingface/datasets/json/default-e3ff36a1d8fe78df/0.0.0/ab573428e7a11a7e23eebd41a2a71665ac3789ce311cbad7049572034a9bda05/json-train.arrow'}], 'test': [{'filename': '/Users/aitormedrano/.cache/huggingface/datasets/json/default-e3ff36a1d8fe78df/0.0.0/ab573428e7a11a7e23eebd41a2a71665ac3789ce311cbad7049572034a9bda05/json-test.arrow'}]}

# squad_dataset.save_to_disk("squad_train_test")

for split, dataset in squad_dataset.items():
    dataset.to_json(f"squad_{split}.jsonl")

from datasets import load_from_disk
squad_disk = load_from_disk("squad_train_test")
print(squad_disk)