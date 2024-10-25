import gradio as gr

def mostrarVideo(input_img):
    return input_img

demo = gr.Interface(mostrarVideo, gr.Video(), "video")
demo.launch()