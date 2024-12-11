import gradio as gr
import matplotlib.pyplot as plt

def plt_plot():
    x = ["PS4", "XBox Series X", "PS5", "Nintendo Switch"]
    y = [68, 73, 82, 74]

    plt.rcParams['figure.figsize'] = 6,4

    plt.title("Ventas de consolas")
    plt.xlabel("Consolas")
    plt.ylabel("Millones de unidades")
    plt.legend(loc="upper left")
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(x, y)

    return fig

demo = gr.Interface(fn=plt_plot, inputs=None, outputs=gr.Plot())

demo.launch()