import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk

# --- Sygnały wejściowe ---
def input_rectangular(t, amplitude):
    return amplitude if (t % 2.0) < 1.0 else 0.0

def input_triangular(t, amplitude):
    period = 2.0
    return amplitude * (1 - abs((t % period) - period / 2) / (period / 2))

def input_sinus(t, amplitude):
    return amplitude * np.sin(2 * np.pi * t)

# --- Równania układu ---
def motor_dynamics(t, x, u_func, R, L, K_e, K_t, J, k):
    i, theta, omega = x
    u = u_func(t)
    di_dt = (u - R * i - K_e * omega) / L
    dtheta_dt = omega
    domega_dt = (K_t * i - k * theta) / J
    return [di_dt, dtheta_dt, domega_dt]

# --- Symulacja i wykresy ---
def simulate_and_plot(R, L, K_t, K_e, J, k, A, signal_type):
    if signal_type == 'prostokat':
        u_func = lambda t: input_rectangular(t, A)
    elif signal_type == 'trojkat':
        u_func = lambda t: input_triangular(t, A)
    else:  
        u_func = lambda t: input_sinus(t, A)

    x0 = [0.0, 0.0, 0.0]
    t_span = (0, 5)
    t_eval = np.linspace(*t_span, 1000)

    sol = solve_ivp(lambda t, x: motor_dynamics(t, x, u_func, R, L, K_e, K_t, J, k), t_span, x0, t_eval=t_eval)
    u_vals = [u_func(t) for t in sol.t]

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(sol.t, u_vals, color='magenta')
    plt.title('Napięcie wejściowe u(t) [V]')
    plt.ylabel('Napięcie (V)')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(sol.t, sol.y[0], color='magenta')
    plt.title('Prąd i(t) [A]')
    plt.ylabel('Prąd (A)')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(sol.t, sol.y[2], color='magenta')
    plt.title('Prędkość kątowa ω(t) [rad/s]')
    plt.xlabel('Czas (s)')
    plt.ylabel('Prędkość (rad/s)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# --- GUI tkinter ---
def start_simulation():
    R = float(entry_R.get())
    L = float(entry_L.get())
    K_t = float(entry_Kt.get())
    K_e = float(entry_Ke.get())
    J = float(entry_J.get())
    k = float(entry_k.get())
    A = float(entry_A.get())
    signal_type = signal_var.get()
    simulate_and_plot(R, L, K_t, K_e, J, k, A, signal_type)

root = tk.Tk()
root.title("Symulacja silnika DC")

fields = [
    ("R [Ohm]", "2.0"),
    ("L [H]", "0.5"),
    ("K_t [Nm/A]", "0.1"),
    ("K_e [Vs/rad]", "0.1"),
    ("J [kg·m²]", "0.02"),
    ("k [Nm/rad]", "0.1"),
    ("Amplituda [V]", "10.0")
]

entries = []
for i, (label, default) in enumerate(fields):
    tk.Label(root, text=label).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.insert(0, default)
    entry.grid(row=i, column=1)
    entries.append(entry)

entry_R, entry_L, entry_Kt, entry_Ke, entry_J, entry_k, entry_A = entries

tk.Label(root, text="Typ sygnału").grid(row=len(fields), column=0)
signal_var = tk.StringVar()
signal_menu = ttk.Combobox(root, textvariable=signal_var)
signal_menu['values'] = ['prostokat', 'trojkat', 'sinus']
signal_menu.current(0)
signal_menu.grid(row=len(fields), column=1)

tk.Button(root, text="Symuluj", command=start_simulation).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

root.mainloop()
