import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parametry układu
#DODAC MOZLIWOSC ZMIANY Z JAKIEGOS MENU
R = float(input("Podaj wartosc rezystancji: "))
L = float(input("Podaj wartosc indukcojnosci: "))
#2R = 2.0          # rezystancja (Ohm)
#L = 0.5          # indukcyjność (H)2
K_t = 0.1        # stała momentu obrotowego (Nm/A)
K_e = 0.1        # stała siły elektromotorycznej (Vs/rad)
J = 0.02         # moment bezwładności wirnika (kg*m^2)
k = 0.1          # stała sprężystości wału (Nm/rad)

# Równania stanu
def motor_dynamics(t, x, u_func):
    i, theta, omega = x
    u = u_func(t)

    di_dt = (u - R * i - K_e * omega) / L
    dtheta_dt = omega
    domega_dt = (K_t * i - k * theta) / J

    return [di_dt, dtheta_dt, domega_dt]

# Definicje sygnałów wejściowych
def input_rectangular(t):
    return 10.0 if 0 <= t <= 1 else 0.0

def input_triangular(t):
    period = 2.0
    return 10.0 * (1 - abs((t % period) - period/2) / (period/2))

def input_harmonic(t):
    return 10.0 * np.sin(2 * np.pi * 1.0 * t)

# Wybór sygnału wejściowego
u_func = input_rectangular  # zmień na input_triangular lub input_harmonic

# Warunki początkowe
x0 = [0.0, 0.0, 0.0]  # prąd, kąt, prędkość kątowa

# Czas symulacji
t_span = (0, 5)
t_eval = np.linspace(*t_span, 1000)

# Rozwiązanie układu równań
solution = solve_ivp(lambda t, x: motor_dynamics(t, x, u_func), t_span, x0, t_eval=t_eval)

# Wykres wyników3
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(solution.t, [u_func(t) for t in solution.t])
plt.title('Napięcie wejściowe u(t) [V]')
plt.ylabel('Napięcie (V)')

plt.subplot(3, 1, 2)
plt.plot(solution.t, solution.y[0])
plt.title('Prąd i(t) w obwodzie [A]')
plt.ylabel('Prąd (A)')

plt.subplot(3, 1, 3)
plt.plot(solution.t, solution.y[2])
plt.title('Prędkość kątowa wału ω(t) [rad/s]')
plt.xlabel('Czas (s)')
plt.ylabel('Prędkość (rad/s)')

plt.tight_layout()
plt.show()