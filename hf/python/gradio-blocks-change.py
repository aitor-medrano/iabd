import gradio as gr

def modifica(nombre):
    return f"¡Bienvenido a Gradio, {nombre}!"

with gr.Blocks() as demo:
    gr.Markdown("Escribe debajo y comprueba la salida")
    with gr.Row():
        inp = gr.Textbox(placeholder="¿Cómo te llamas?", label="Entrada")
        out = gr.Textbox(label="Salida")

    inp.change(fn=modifica, inputs=inp, outputs=out)

demo.launch()