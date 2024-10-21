import numpy as np
import gradio as gr

def blueHue(input_img):
    blue_hue_filter = np.array([
            [0.272, 0.534, 0.131], 
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]])
    blue_hue_img = input_img.dot(blue_hue_filter.T)
    blue_hue_img /= blue_hue_img.max()
    return blue_hue_img

demo = gr.Interface(blueHue, gr.Image(height=300, width=200), "image")
demo.launch()