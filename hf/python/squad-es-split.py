from datasets import load_dataset

squad_dataset = load_dataset("json", data_files="train-v2.0-es.json", field="data", split="train")
squad_split_dataset = squad_dataset.train_test_split(test_size=0.1)
print(squad_split_dataset)