from datasets import load_dataset

squad_dataset = load_dataset("squad_es", "v2.0.0", split="train")

print(squad_dataset)
# Dataset({
#     features: ['id', 'title', 'context', 'question', 'answers'],
#     num_rows: 130313
# })

print(squad_dataset[0])
squad_dataset.set_format("pandas")
df = squad_dataset[:]
print(df.shape)

# Otra forma
df2 = squad_dataset.to_pandas()
# print(df2.info())
print(df2.groupby("title")["answers"].count().nlargest(5))