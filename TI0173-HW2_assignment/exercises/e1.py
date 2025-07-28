from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import control as co
from modules.read_data import read
from modules.view_plot import advanced_plot, step_response_plot
import warnings
warnings.filterwarnings("ignore")

path = "D:\\Area de trabalho\\Faculdade\\Disciplinas\\2025.1\\Sistema de Controle\\TI0173-HW2_assignment\\data\\"
system_A = "HW2_ex1_dataA.csv"
system_B = "HW2_ex1_dataB.csv"

def item1(step_response_A:pd.DataFrame, step_response_B:pd.DataFrame):
    t_A, y_A = step_response_A.iloc[:,0], step_response_A.iloc[:,1]
    t_B, y_B = step_response_B.iloc[:,0], step_response_B.iloc[:,1]

    step_response_plot(y_A, t_A, "System A", save=True)
    step_response_plot(y_B, t_B, "System B", save=True)

def item2(step_response_A, step_response_B):
    t_A, y_A = step_response_A.iloc[:,0], step_response_A.iloc[:,1]
    t_B, y_B = step_response_B.iloc[:,0], step_response_B.iloc[:,1]

    percentual_estavel_1 = 0.3
    percentual_estavel_2 = 0.1
    indice_inicio_estavel_A = int(len(y_A) * (1 - percentual_estavel_1)) # 20 * 1-0.3
    indice_inicio_estavel_B = int(len(y_B) * (1 - percentual_estavel_2))

    y_inf_A = np.mean(y_A[indice_inicio_estavel_A:])
    print(f"Valor Final Estimado (Sistema A): {y_inf_A:.4f}")

    y_inf_B = np.mean(y_B[indice_inicio_estavel_B:])
    print(f"Valor Final Estimado (Sistema B): {y_inf_B:.4f}")

    print("\n--- Análise do Sistema A (Exponencial Crescente - 1 ordem) ---")
    target_tau_A = y_inf_A * 0.632 # Encontrar a Constante de Tempo (tau)
    index_tau_A = np.where(y_A >= target_tau_A)[0][0] # Encontrar o primeiro índice onde a amplitude y_A ultrapassa o valor alvo
    
    # 1. Calcular a Constante de Tempo (tau)
    tau_A = t_A[index_tau_A]
    print(f"A resposta atinge 63.2% ({target_tau_A:.2f}) do valor final em t = {tau_A:.4f} s")
    print(f"Constante de Tempo Estimada (τ_A): {tau_A:.4f} s")

    # 2. Calcular Tempo de Acomodação (Ts)
    Ta_A_tau = 4 * tau_A
    print(f"Tempo de Acomodação (Ts ≈ 4τ): {Ta_A_tau:.4f} s")

    # 3. Calcular o Tempo de Subida (Ts)
    Ts_A_tau = 2.2 * tau_A
    print(f"Tempo de Subida (Ts ≈ 2.2τ): {Ts_A_tau:.4f} s")

    index_pico_A = np.argmax(y_A) # Encontra o índice do valor máximo em y_A
    y_pico_A = y_A[index_pico_A] # O valor máximo é o valor de y_A nesse índice
    Tp_A = t_A[index_pico_A] # O tempo de pico é o valor de t_A no mesmo índice
    print(f"Valor de Pico (y_pico_A): {y_pico_A:.4f}")
    print(f"Tempo de Pico (Tp_A): {Tp_A:.4f} s")

    # 4. Calcular Porcentagem de Overshoot (%UP)
    UP_A = ((y_pico_A - y_inf_A) / y_inf_A) * 100
    print(f"Porcentagem de Overshoot (%UP): {UP_A:.2f}%")

    print("\n--- Análise do Sistema B (Subamortecido - 2 ordem) ---")

    target_tau_B = y_inf_B * 0.632
    index_tau_B = np.where(y_B >= target_tau_B)[0][0] # Encontrar o primeiro índice onde a amplitude y_B ultrapassa o valor alvo

    # 1. Calcular a Constante de Tempo (tau)
    tau_B = t_B[index_tau_B]
    print(f"A resposta atinge 63.2% ({target_tau_B:.2f}) do valor final em t = {tau_B:.4f} s")
    print(f"Constante de Tempo Estimada (τ_B): {tau_B:.4f} s")

    # 2. Calcular Tempo de Acomodação (Ta)
    Ta_B_tau = 4 * tau_B
    print(f"Tempo de Acomodação (Ta ≈ 4τ): {Ta_B_tau:.4f} s")

    # 3. Calcular o Tempo de Subida (Ts)
    Ts_B_tau = 2.2 * tau_B
    print(f"Tempo de Subida (Ts ≈ 2.2τ): {Ts_B_tau:.4f} s")

    # 3. Encontrar o Tempo de Pico (Tp) e o Valor de Pico (y_pico)
    index_pico_B = np.argmax(y_B) # Encontra o índice do valor máximo em y_B
    y_pico_B = y_B[index_pico_B] # O valor máximo é o valor de y_B nesse índice
    Tp_B = t_B[index_pico_B] # O tempo de pico é o valor de t_B no mesmo índice
    print(f"Valor de Pico (y_pico_B): {y_pico_B:.4f}")
    print(f"Tempo de Pico (Tp_B): {Tp_B:.4f} s")

    # 3. Calcular Porcentagem de Overshoot (%UP)
    UP_B = ((y_pico_B - y_inf_B) / y_inf_B) * 100
    print(f"Porcentagem de Overshoot (%UP): {UP_B:.2f}%")

def item3(step_response_A, step_response_B):
    t_A, y_A = step_response_A.iloc[:,0], step_response_A.iloc[:,1]
    t_B, y_B = step_response_B.iloc[:,0], step_response_B.iloc[:,1]

    print("--- Iniciando Validação do Sistema A ---")
    # 1. Definir a função de transferência TA(s) que estimamos
    # TA(s) = 36.21/7.4s+1
    TA = co.tf([36.21], [7.4, 1])

    num_pontos = len(t_A)
    tempo_ideal_A = np.linspace(t_A.iloc[0], t_A.iloc[-1], num_pontos)

    # 3. Calcular a resposta ao degrau do modelo TA(s)
    print(f"TA: {TA}")
    print(f"t_A: {t_A}")
    yout_A, T_out_A = co.step_response(TA, T=tempo_ideal_A)

    # 4. Plotar a comparação
    advanced_plot(t_A, y_A, T_out_A, yout_A, filename="modelo_estimado_A_e1", title="Validação do Modelo para o Sistema A")

    print("\n--- Iniciando Validação do Sistema B ---")
        
    # 1. Definir a função de transferência TB(s) que estimamos
    # TB(s) = 13.46 / (s^2 + 0.610s + 4.486)
    numerador_B = [13.46]
    denominador_B = [1, 0.610, 4.486]
    TB = co.tf(numerador_B, denominador_B) 

    num_pontos = len(t_B)
    tempo_ideal_B = np.linspace(t_B.iloc[0], t_B.iloc[-1], num_pontos)

 
    # 2. Calcular a resposta ao degrau do modelo TB(s)
    yout_B, T_out_B = co.step_response(TB, T=tempo_ideal_B)

    # 3. Plotar a comparação
    advanced_plot(t_B, y_B, T_out_B, yout_B, filename="modelo_estimado_B_e1", title="Validação do Modelo para o Sistema B")

def main_e1():
    step_response_A = read(path + system_A)
    step_response_B = read(path + system_B)

    print(f"Step Response A (shape): {step_response_A.shape}")
    print(f"Step Response B (shape): {step_response_B.shape}")
    
    print("Item 1:")
    item1(step_response_A, step_response_B)

    print("Item 2:")
    item2(step_response_A, step_response_B)

    print("Item 3:")
    item3(step_response_A, step_response_B)