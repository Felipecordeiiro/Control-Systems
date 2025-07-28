import control as ct
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Análise do Código
# =============================================================================
# Este script simula o comportamento de um conversor CC-CC (DC-DC converter).
# O objetivo é comparar a resposta do sistema em duas situações:
# 1. Malha Aberta (Open-loop): Como a tensão de saída reage a uma pequena
#    perturbação no "duty cycle" (ciclo de trabalho do PWM) sem um controlador.
# 2. Malha Fechada (Closed-loop): Como a tensão de saída se comporta ao
#    receber uma nova referência (um novo valor desejado), agora com um
#    controlador proporcional (ganho K) para corrigir o erro.
#
# A planta Gvd(s) representa a função de transferência "controle-para-saída",
# ou seja, como a tensão de saída (Vo) muda em resposta a variações no
# ciclo de trabalho (d). O ganho DC negativo de Gvd é característico de
# conversores inversores como o Buck-Boost.

# --- 1. Parâmetros do Sistema ---
Vi = 24.0      # Tensão de entrada [V]
L = 20e-6      # Indutância [H]
C = 80e-6      # Capacitância [F]
Ro = 4.0       # Resistência de carga [Ohms]
D = 0.4        # Ciclo de trabalho (Duty cycle) em regime permanente
# Tensão de saída em regime permanente (ponto de operação)
Vo = -Vi * D / (1 - D)  # Vo = -16V

# --- 2. Função de Transferência Controle-para-Saída ---
# Gvd(s) = Vo(s) / d(s)
# No MATLAB: num = -Vi; den = [L*C, L/Ro, (1-D)^2];
num = [-Vi]
den = [L * C, L / Ro, (1 - D)**2]
Gvd = ct.tf(num, den)

print("Função de Transferência Gvd(s):")
print(Gvd)

# --- 3. Projeto do Controlador Proporcional ---
# O objetivo é ter um erro de 10% em regime permanente.
# Para um sistema com realimentação unitária, o erro (ess) para uma entrada degrau é:
# ess = 1 / (1 + Kp), onde Kp é a constante de erro de posição.
# 0.10 = 1 / (1 + Kp) => 1 + Kp = 10 => Kp_des = 9
Kp_des = 9.0

# A constante de erro de posição é Kp = lim(s->0) C(s)*G(s)
# Para C(s) = K (controlador P), temos Kp = K * Gvd(0)
# K = Kp_des / Gvd(0).
# Gvd(0) é o ganho DC, que é negativo. Para ter realimentação negativa,
# o ganho total do laço (K * Gvd(0)) deve ser positivo, então K também deve ser negativo.
# No código MATLAB, ele usa abs() e adiciona o sinal, o que é o mesmo que não usar abs().
# dcgain = Gvd(0)
dc_gain_gvd = ct.dcgain(Gvd)
K = Kp_des / dc_gain_gvd

print(f'\nGanho do Controlador K = {K:.4f}')

# --- 4. Parâmetros da Simulação ---
step_time = 0.001  # Tempo em que o degrau é aplicado [s]
t_sim = 0.02       # Tempo total da simulação [s]
t = np.linspace(0, t_sim, 10000)
d_step = 0.05      # Amplitude do degrau no duty cycle (malha aberta)

# --- 5. Simulação em Malha Aberta ---
# Simula o efeito de uma perturbação no duty cycle
u_ol = d_step * (t >= step_time)
_, y_ol = ct.forced_response(Gvd, t, u_ol)
Vo_ol = Vo + y_ol # A resposta é uma variação em torno do ponto de operação Vo

# --- 6. Simulação em Malha Fechada ---
# O controlador é apenas um ganho K
C_tf = ct.tf([K], [1])
# A realimentação é unitária (H=1)
T = ct.feedback(C_tf * Gvd, 1)

# Simula o efeito de um degrau na referência de tensão
# Queremos aumentar a tensão de -16V para -15V, um degrau de +1V
V_ref_step = 1.0
u_cl = V_ref_step * (t >= step_time)
_, y_cl = ct.forced_response(T, t, u_cl)
Vo_cl = Vo + y_cl # A resposta é uma variação em torno do ponto de operação Vo

# --- 7. Métricas de Desempenho ---
# Malha Aberta
ss_ol = Vo + d_step * dc_gain_gvd

# Malha Fechada
ss_cl = np.mean(Vo_cl[-500:]) # Média dos últimos 500 pontos
desired_final = Vo + V_ref_step

# Erro em Regime Estacionário
ess_abs = desired_final - ss_cl
ess_percent = 100 * ess_abs / V_ref_step

# Overshoot (para um degrau negativo, é um "undershoot")
# A tensão começa em -16V e vai para -15.1V. O overshoot ocorre se a tensão
# for para um valor MAIS NEGATIVO que -15.1V.
if Vo_cl[0] > ss_cl: # Degrau negativo (ex: -16V para -15V)
    min_val = np.min(Vo_cl)
    overshoot = 100 * abs(min_val - ss_cl) / abs(Vo_cl[0] - ss_cl)
else: # Degrau positivo
    max_val = np.max(Vo_cl)
    overshoot = 100 * (max_val - ss_cl) / (ss_cl - Vo_cl[0])

# Tempo de Subida (10% a 90%)
total_change = final_val = ss_cl - Vo_cl[0]
val_10 = Vo_cl[0] + 0.1 * total_change
val_90 = Vo_cl[0] + 0.9 * total_change
try:
    idx_10 = np.where(Vo_cl >= val_10)[0][0]
    idx_90 = np.where(Vo_cl >= val_90)[0][0]
    rise_time = (t[idx_90] - t[idx_10]) * 1e6  # em µs
except IndexError:
    rise_time = np.nan # Não foi possível calcular

# Tempo de Acomodação (critério de 2%)
tolerance = 0.02 * abs(total_change)
# Encontra o último índice onde a resposta está FORA da tolerância
try:
    settling_idx = np.where(np.abs(Vo_cl - ss_cl) > tolerance)[0][-1]
    # O tempo de acomodação é o tempo a partir do degrau
    settling_time = (t[settling_idx] - step_time) * 1e6 # em µs
except IndexError:
    settling_time = np.nan # Já está acomodado

# --- 8. Plotar e Salvar Resultados ---

# Plot 1: Análise da Resposta em Malha Fechada (Sinal Vermelho)
plt.figure(figsize=(12, 7))
plt.plot(t * 1000, Vo_cl, 'r', linewidth=1.5, label='Malha Fechada (degrau na referência)')
plt.axvline(step_time * 1000, color='k', linestyle='--', linewidth=1, label='Início do Degrau')
plt.axhline(desired_final, color='g', linestyle='--', linewidth=1.5, label=f'Tensão Desejada ({desired_final:.2f} V)')
plt.axhline(ss_cl, color='r', linestyle='--', linewidth=1.5, label=f'Regime Malha Fechada ({ss_cl:.2f} V)')
plt.grid(True)
plt.title('Análise da Resposta em Malha Fechada')
plt.xlabel('Tempo [ms]')
plt.ylabel('Tensão de Saída Vo [V]')
plt.legend(loc='best')
# Salva a figura antes de exibi-la
plt.savefig('./TI0173-PW/results/resposta_malha_fechada.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 2: Análise da Resposta em Malha Aberta (Sinal Azul)
plt.figure(figsize=(12, 7))
plt.plot(t * 1000, Vo_ol, 'b', linewidth=1.5, label='Malha Aberta (degrau no duty cycle)')
plt.axvline(step_time * 1000, color='k', linestyle='--', linewidth=1, label='Início do Degrau')
plt.axhline(Vo, color='gray', linestyle='--', label=f'Tensão Inicial ({Vo:.2f} V)')
plt.axhline(ss_ol, color='b', linestyle='--', linewidth=1.5, label=f'Regime Malha Aberta ({ss_ol:.2f} V)')
plt.grid(True)
plt.title('Análise da Resposta em Malha Aberta')
plt.xlabel('Tempo [ms]')
plt.ylabel('Tensão de Saída Vo [V]')
plt.legend(loc='best')
# Salva a figura antes de exibi-la
plt.savefig('./TI0173-PW/results/resposta_malha_aberta.png', dpi=300, bbox_inches='tight')
plt.show()


# --- 9. Exibir Métricas ---
print('\n===== Sistema em Malha Aberta =====')
print(f'Degrau no Duty Cycle: {d_step:.4f}')
print(f'Variação em Regime Permanente: {d_step * dc_gain_gvd:.3f} V')
print(f'Tensão Final: {ss_ol:.3f} V')

print('\n===== Sistema em Malha Fechada =====')
print(f'Degrau na Referência: {V_ref_step:.2f} V')
print(f'Kp Alcançado = {-K * abs(dc_gain_gvd):.3f} (Alvo = {Kp_des})')
print(f'Erro em Regime Permanente: {ess_abs:.3f} V ({ess_percent:.1f}%)')
print(f'Overshoot: {overshoot:.1f}%')
print(f'Tempo de Subida: {rise_time:.2f} µs')
print(f'Tempo de Acomodação: {settling_time:.2f} µs')
