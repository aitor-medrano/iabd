import gradio as gr
from diffusers import StableDiffusion3Pipeline
import torch

def stable(prompt):
    pipeline = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16)
    pipeline.to("cuda")
    return pipeline(prompt,
        negative_prompt="",
        num_inference_steps=28,
        guidance_scale=7.0).images[0]

demo = gr.Interface(fn=stable, inputs="text", outputs="image")
demo.launch()