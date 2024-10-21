from transformers import AutoProcessor, BarkModel
import gradio as gr

model_name="suno/bark-small"

processor = AutoProcessor.from_pretrained(model_name)
model = BarkModel.from_pretrained(model_name)

voice_preset = "v2/es_speaker_0"

def tts(frase):
    inputs = processor(frase, voice_preset=voice_preset)

    audio_array = model.generate(**inputs, pad_token_id=100)
    audio_array = audio_array.cpu().numpy().squeeze()

    sample_rate = model.generation_config.sample_rate

    return sample_rate,audio_array

demo = gr.Interface(
    tts,
    inputs=gr.Text(label="Teclea el texto a pronunciar"),
    outputs=gr.Audio(label="audio generado"),
    title="De texto a voz",
)

demo.launch()
