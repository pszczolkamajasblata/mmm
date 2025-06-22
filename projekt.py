import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons
from scipy.signal import sawtooth


def input_rectangular(t, A, period):
    return A if (t % period) < (period / 2) else 0.0

def input_triangular(t, A, period):
    return A * (sawtooth(2 * np.pi * t / period, width=0.5) + 1) / 2

def input_sinus(t, A, period):
    return A * np.sin(2 * np.pi * t / period)

def motor_dynamics(t, x, u, R, L, Ke, Kt, J, k):
    i, theta, omega = x
    di_dt = (u - R * i - Ke * omega) / L
    dtheta_dt = omega
    domega_dt = (Kt * i - k * theta) / J
    return [di_dt, dtheta_dt, domega_dt]

def parse_inputs():
    try:
        return [float(tb.text) for tb in textboxes]
    except ValueError:
        return None

def update(_):
    vals = parse_inputs()
    if vals is None or any(x == 0 for x in vals[:-1]):
        for ax in axs:
            ax.clear()
            ax.text(0.5, 0.5, 'Błędne dane', ha='center', va='center', color='red', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
        fig.canvas.draw_idle()
        return

    R, L, Kt, Ke, J, k, A, period, t_end = vals
    signal = radio.value_selected
    input_func = {
        'prostokat': input_rectangular,
        'trojkat': input_triangular,
        'sinus': input_sinus
    }[signal]

    dt = 0.001
    t = np.arange(0, t_end, dt)
    i_vals, theta_vals, omega_vals, u_vals = [], [], [], []
    x = [0.0, 0.0, 0.0] # [i, theta, omega]

    for ti in t:
        u = input_func(ti, A, period)
        dx = motor_dynamics(ti, x, u, R, L, Ke, Kt, J, k)
        x = [x[j] + dx[j] * dt for j in range(3)]
        i_vals.append(x[0])
        theta_vals.append(x[1])
        omega_vals.append(x[2])
        u_vals.append(u)

    axs[0].clear()
    axs[0].plot(t, u_vals, color='magenta')
    axs[0].set_title("Napięcie u(t)")

    axs[1].clear()
    axs[1].plot(t, i_vals, color='magenta')
    axs[1].set_title("Prąd i(t)")

    axs[2].clear()
    axs[2].plot(t, omega_vals, color='magenta')
    axs[2].set_title("Prędkość kątowa ω(t)")
    axs[2].set_xlabel("Czas [s]")

    for ax in axs:
        ax.grid(True)

    fig.canvas.draw_idle()

fig, axs = plt.subplots(3, 1, figsize=(14, 18)) 
plt.subplots_adjust(left=0.5, bottom=0.1, hspace=0.6)


mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())  


text_defs = [
    ('R', 1.0), ('L', 1.0), ('Kt', 1.0), ('Ke', 1.0),
    ('J', 1.0), ('k', 100.0), ('A', 1.0), ('period', 1.0), ('time', 10.0)
]

textboxes = []
for i, (label, val) in enumerate(text_defs):
    ax = plt.axes([0.05, 0.92 - i * 0.05, 0.3, 0.03])
    tb = TextBox(ax, f'{label}: ', initial=str(val))
    tb.on_submit(update)
    textboxes.append(tb)

radio_ax = plt.axes([0.05, 0.02, 0.3, 0.12], facecolor='pink')
radio = RadioButtons(radio_ax, ('prostokat', 'trojkat', 'sinus'))
radio.on_clicked(update)

update(None)
plt.show()
