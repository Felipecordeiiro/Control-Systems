import os
from matplotlib import pyplot as plt


def common_plot(x, t, xlabel, ylabel, title:str, filename=None, save=False):
    fig, ax = plt.subplots()
    ax.plot(t, x)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.legend()
    plt.show()
    plt.close(fig)
    if save:
        path_results = "./TI0173-HW2_assignment/results"
        filename = f'{filename}.png'
        path_save = os.path.join(path_results, filename)
        save_plot(fig, path_save)

def advanced_plot(t_A, y_A, T_out_A, yout_A, title=None, filename=None, save=True):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(t_A, y_A, 'o', markersize=4, label='Dados Originais')
    ax.plot(yout_A, T_out_A, '-', linewidth=2.5, color='red', label=f'Modelo Estimado')
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    plt.show()
    if save:
        path_results = "./TI0173-HW2_assignment/results"
        filename = f'{filename}.png'
        path_save = os.path.join(path_results, filename)
        save_plot(fig, path_save)


def step_response_plot(x, t, title:str, save=False):
    fig, ax = plt.subplots()
    ax.plot(t, x)
    ax.set_title('Unit Step Response - ' + title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    plt.legend()
    plt.show()
    plt.close(fig)
    if save:
        title = title.replace(" ", "_").lower()
        path_results = "./TI0173-HW2_assignment/results"
        filename = f'step_response_{title}.png'
        path_save = os.path.join(path_results, filename)
        save_plot(fig, path_save)

def save_plot(fig, filename):
    fig.savefig(filename)
    plt.close(fig)