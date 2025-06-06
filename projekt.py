import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from scipy.signal import sawtooth

#sygnały wejściowe
def input_rectangular_func(t, amplitude, period):
    return amplitude if (t % period) < (period / 2) else 0.0

def input_triangular_func(t, amplitude, period):
    return amplitude * (sawtooth(2 * np.pi * t / period, width=0.5) + 1) / 2

def input_sinus_func(t, amplitude, period):
    return amplitude * np.sin(2 * np.pi * t / period)

#równania układu
def motor_dynamics(t, x, u, R, L, K_e, K_t, J, k):
    i, theta, omega = x
    di_dt = (u - R * i - K_e * omega) / L
    dtheta_dt = omega
    domega_dt = (K_t * i - k * theta) / J
    return [di_dt, dtheta_dt, domega_dt]

#symulacja - metoda eulera
def simulate_and_plot(R, L, K_t, K_e, J, k, A, signal_type, period, t_end):
    if signal_type == 'prostokat':
        input_func = input_rectangular_func
    elif signal_type == 'trojkat':
        input_func = input_triangular_func
    else:
        input_func = input_sinus_func

    t_start, dt = 0.0, 0.001
    t_values = np.arange(t_start, t_end + dt, dt)

    #inicjalizacja zmiennych
    x = [0.0, 0.0, 0.0]  #[i, theta, omega]
    i_vals, theta_vals, omega_vals, u_vals = [], [], [], []

    for t in t_values:
        u = input_func(t, A, period)
        dx = motor_dynamics(t, x, u, R, L, K_e, K_t, J, k)
        
        i = x[0] + dx[0] * dt
        theta = x[1] + dx[1] * dt
        omega = x[2] + dx[2] * dt
        x = [i, theta, omega]

        i_vals.append(x[0])
        theta_vals.append(x[1])
        omega_vals.append(x[2])
        u_vals.append(u)


    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t_values, u_vals, color='magenta')
    plt.title('Napięcie wejściowe u(t) [V]')
    plt.ylabel('Napięcie (V)')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(t_values, i_vals, color='magenta')
    plt.title('Prąd i(t) [A]')
    plt.ylabel('Prąd (A)')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(t_values, omega_vals, color='magenta')
    plt.title('Prędkość kątowa ω(t) [rad/s]')
    plt.xlabel('Czas (s)')
    plt.ylabel('Prędkość (rad/s)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

#GUI
def start_simulation():
    R = float(entry_R.get())
    L = float(entry_L.get())
    K_t = float(entry_Kt.get())
    K_e = float(entry_Ke.get())
    J = float(entry_J.get())
    k = float(entry_k.get())
    A = float(entry_A.get())
    period = float(entry_period.get())
    t_end = float(entry_t_end.get())
    signal_type = signal_var.get()
    simulate_and_plot(R, L, K_t, K_e, J, k, A, signal_type, period, t_end)

root = tk.Tk()
root.title("Symulacja silnika DC")

fields = [
    ("R [Ohm]", "2.0"),
    ("L [H]", "0.5"),
    ("K_t [Nm/A]", "0.1"),
    ("K_e [Vs/rad]", "0.1"),
    ("J [kg·m²]", "0.02"),
    ("k [Nm/rad]", "0.1"),
    ("Amplituda [V]", "10.0"),
    ("Okres sygnału [s]", "2.0"),
    ("Czas symulacji [s]", "5.0")
]

entries = []
for i, (label, default) in enumerate(fields):
    tk.Label(root, text=label).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.insert(0, default)
    entry.grid(row=i, column=1)
    entries.append(entry)

entry_R, entry_L, entry_Kt, entry_Ke, entry_J, entry_k, entry_A, entry_period, entry_t_end = entries

tk.Label(root, text="Typ sygnału").grid(row=len(fields), column=0)
signal_var = tk.StringVar()
signal_menu = ttk.Combobox(root, textvariable=signal_var)
signal_menu['values'] = ['prostokat', 'trojkat', 'sinus']
signal_menu.current(0)
signal_menu.grid(row=len(fields), column=1)

tk.Button(root, text="Symulacja", command=start_simulation).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

root.mainloop()
