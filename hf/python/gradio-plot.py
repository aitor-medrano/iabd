import gradio as gr
import pandas as pd

# Función que convierte el DataFrame en un formato adecuado para gr.BarPlot
def create_barplot_from_df():
    data = {
        "Frutas": ["Manzanas", "Bananas", "Naranjas"],
        "Cantidad": [10, 15, 7]
    }
    df = pd.DataFrame(data)
    
    # Devolver los datos en el formato adecuado para gr.BarPlot
    return df

demo = gr.Interface(fn=create_barplot_from_df, inputs=None, outputs=[gr.BarPlot()])

demo.launch()