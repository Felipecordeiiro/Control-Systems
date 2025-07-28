import numpy as np
import control as co
from control.matlab import *
from matplotlib import pyplot as plt

from modules.view_plot import common_plot

import warnings
warnings.filterwarnings("ignore")

def item1():
    # Definindo as variáveis da equação de estados
    A = np.array([[0, 1], [-5, -2]])
    B = np.array([[0], [2]])
    C = np.array([[0, 1]])
    D = np.array([[0]])
    
    sys_ss = co.ss(A,B,C,D)
    Gs = co.ss2tf(sys_ss)

    print(Gs)
    return Gs

def item2(Gs):
    #Gf = co.feedback(Gs, 1)
    yout, T = co.step_response(Gs)
    #yout, T = step(Gf)
    common_plot(T, yout, xlabel="Time (seconds)", ylabel="c(t)", title="G(s)", filename="Gs_item2", save=True)
    
    plt.figure(figsize=(10, 8))
    co.pzmap(Gs, grid=True, plot=True, title='Pole-Zero Map of System')
    plt.savefig("./TI0173-HW2_assignment/results/pzmap_e2_item2.png")
    plt.show()

def item3():
    pass

def main_e2():
    
    print("Item 1:")
    Gs = item1()

    print("Item 2:")
    item2(Gs)

    print("Item 3:")
    item3()
