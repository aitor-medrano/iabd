from transformers import pipeline

frase_en = "I like to play basketball and being a geek"

model = f"Helsinki-NLP/opus-mt-en-es"
pipe = pipeline("translation", model=model)
translation = pipe(frase_en)

print(translation[0]['translation_text'])

# pip install gradio transformers torch sentencepiece sacremoses
