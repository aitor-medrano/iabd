import gradio as gr

#app 1
def saluda(nombre):
    return "¡Hola " + nombre + "!. Hello Gradio!😎"

app1 =  gr.Interface(fn = saluda, inputs="text", outputs="text")

#app 2
def mensaje(accion):
    return "Hoy vamos a " + accion + " con Gradio"

app2 =  gr.Interface(fn = mensaje, inputs="text", outputs="text")

demo = gr.TabbedInterface([app1, app2], ["Bienvenid@", "¿Qué hacemos?"], "Uso de pestañas")

demo.launch()