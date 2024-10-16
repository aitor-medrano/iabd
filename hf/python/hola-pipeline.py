from transformers import pipeline

pipe = pipeline("text-generation", model="openai-community/gpt2")
result = pipe("What is big data?")
print(result)
# [{'generated_text': "What is big data?\n\nBig data describes all kinds of things and I know who is a big data guy! I'd love to talk about anything related to big data science or what I hear in our labs, but that's really boring."}]

trad = pipeline("text2text-generation", model="google/flan-t5-base")
result = trad("translate from spanish to english: Me encanta disfrutar las vacaciones en la playa")
print(result)
# [{'generated_text': 'I love having holidays on the beach'}]