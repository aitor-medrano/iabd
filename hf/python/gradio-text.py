import gradio as gr

def muestraTexto(frase):
    return frase

demo = gr.Interface(muestraTexto, gr.Text(), "text")
#alternatively use gr.TextBox()
demo.launch()