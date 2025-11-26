import numpy as np
import matplotlib.pyplot as plt

# Parâmetros conforme valores calculados fornecidos pelo usuário
Vin = 50.0            # Tensão de entrada (V)
L = 1.20e-3          # Indutância do indutor (H) = 1.20 mH
R = 4                # Resistência de carga (Ω) = 4 Ω
C = 15.60e-6         # Capacitância do capacitor de saída (F) = 15.60 µF
Fs = 20e3            # Frequência de chaveamento (Hz) = 20 kHz
D = 0.4              # Duty cycle (40%)
Ts = 1 / Fs          # Período de chaveamento (s)

# Valor médio de saída (esperado)
Voutmed = D * Vin     # 20 V

# Tempo de simulação: 5 ms para ver o amortecimento
t_end = 5e-3       # 5 ms
dt = Ts / 200      # subdividindo cada período em 200 passos
t = np.arange(0, t_end, dt)

# Vetores de simulação
iL = np.zeros_like(t)     # Corrente do indutor
vout = np.zeros_like(t)   # Tensão do capacitor/saída

# Condições iniciais
iL[0] = 0.0
vout[0] = 0.0

# Loop de integração (Euler explícito)
for k in range(len(t) - 1):
    t_cycle = t[k] % Ts
    
    # Determinar aberto ou fechado
    if t_cycle < D * Ts:
        # Estado ON: Chave fechada
        vL = Vin - vout[k]   # Tensão no indutor = Vin - Vout
        iC = -vout[k] / R    # Corrente no capacitor = - corrente na carga
    else:
        # Estado OFF: Chave aberta
        vL = -vout[k]        # Tensão no indutor = -Vout
        iC = iL[k] - vout[k] / R  # Corrente no capacitor = iL - iR

    # MÉTODO EULER EXPLÍCITO - Atualizar corrente do indutor
    diL_dt = vL / L  # Derivada: diL/dt = vL/L
    iL[k + 1] = iL[k] + diL_dt * dt

    # MÉTODO EULER EXPLÍCITO - Atualizar tensão do capacitor
    dvC_dt = iC / C  # Derivada: dvC/dt = iC/C
    vout[k + 1] = vout[k] + dvC_dt * dt


# Plot apenas da tensão de saída
plt.figure(figsize=(12, 6))
plt.plot(t * 1e3, vout, 'b-', linewidth=1.5, label='Tensão de Saída (vout)')
plt.axhline(Voutmed, color='red', linestyle='--', label=f'Média Teórica = {Voutmed:.1f} V')
plt.title('Resposta Transitória e Estabilização da Tensão de Saída (50 V → 20 V) - Euler Explícito')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()