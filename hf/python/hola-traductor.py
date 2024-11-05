from transformers import pipeline

frase_en = "I like to play basketball and being a geek"

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
frase_es = pipe(frase_en)

print(frase_es[0]['translation_text'])
# Me gusta jugar al baloncesto y ser un friki