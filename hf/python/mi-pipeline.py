from transformers import pipeline

pipe = pipeline(model="aitor-medrano/iabd_model")
result = pipe("https://s1.elespanol.com/2023/03/10/curiosidades/mascotas/747436034_231551832_1706x1280.jpg")
print(result)