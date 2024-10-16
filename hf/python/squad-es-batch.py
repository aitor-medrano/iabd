from datasets import load_dataset
import time

squad_dataset = load_dataset("squad_es", "v2.0.0", split="train")

def titulo_minus(registro):
    return {"title":registro["title"].lower()}

inicio = time.time()
squad_minus = squad_dataset.map(titulo_minus)
fin = time.time()
print(fin - inicio)

def titulo_minus_batch(batch):
    return {"title":[titulo.lower() for titulo in batch["title"]]}

inicio = time.time()
squad_minus = squad_dataset.map(titulo_minus_batch, batched=True)
fin = time.time()
print(fin - inicio)


print(squad_minus.shuffle(seed=987)["title"][:5])
# ['marshall', 'ascensor', 'kanye', 'bbc televisión', 'florida']
