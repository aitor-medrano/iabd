from datasets import load_dataset

ficheros_datos = {"train": "train-v2.0-es.json", "test": "dev-v2.0-es.json"}
squad_dataset = load_dataset("json", data_files=ficheros_datos, field="data")
squad_dataset = squad_dataset["train"]

def titulo_minus(registro):
    return {"title":registro["title"].lower()}

squad_minus = squad_dataset.map(titulo_minus)
print(squad_minus.shuffle(seed=987)["title"][:5])
# ['marshall', 'ascensor', 'kanye', 'bbc televisión', 'florida']

# Añadimos nueva columna
squad_col_num_parrafos = squad_dataset.map(lambda x: {"num_paragraphs":len(x["paragraphs"])})
# Borramos la antigua
squad_col_num_parrafos = squad_col_num_parrafos.remove_columns("paragraphs")
print(squad_col_num_parrafos.shuffle(seed=987)[:5])
# {'title': ['Marshall', 'Ascensor', 'Kanye', 'BBC Televisión', 'Florida'], 'num_paragraphs': [51, 52, 79, 31, 35]}

squad_num_parrafos_ordenados = squad_col_num_parrafos.sort("num_paragraphs")
print(squad_num_parrafos_ordenados[:3]) # tres primeros
# {'title': ['Tono _ (música)', 'Uva', 'Letra _ case'], 'num_paragraphs': [10, 10, 12]}
print(squad_num_parrafos_ordenados[-3:]) # tres últimos
# {'title': ['American Idol (en inglés).', 'Nueva York', 'Budismo'], 'num_paragraphs': [127, 148, 149]}