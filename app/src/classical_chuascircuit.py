import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from app.src.constants import *


def dv(_, state):
    """Return the derivative of the state vector."""
    x, y, z = state
    f_x = Gb * x + (Ga - Gb) * (np.abs(x + E) - np.abs(x - E)) / 2
    dxdt = 1/C1 * (G*(y - x) - f_x)
    dydt = 1/C2*(G*(x - y) + z)
    dzdt = -y /L
    return [dxdt, dydt, dzdt]

def launch_chua_circuit():
    initial_state = [v1_0, v2_0, i3_0]  # [x, y, z]
    t_span = (0, end)
    t_eval = np.linspace(t_span[0], t_span[1], number)

    solution = solve_ivp(
        dv,
        t_span,
        initial_state,
        t_eval=t_eval,
        method='RK45'
    )

    t = solution.t
    x, y, z = solution.y
    z *= 1000
    fig, ax1 = plt.subplots(figsize=(12, 8), )
    ax1.plot(t, x, label='v1 (V)', color='blue')
    ax1.plot(t, y, label='v2 (V)', color='green')
    ax1.set_title("Classical Chua's circuit with the study's values")
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('U (V)')
    ax2 = ax1.twinx()
    ax2.plot(t, z, label='i3 (mA)', color='orange')
    ax2.set_ylabel('I (mA)', color='orange')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.spines['right'].set_color('orange')
    fig.tight_layout()
    fig.savefig('app/ressources/export/classical_chuascircuit_time.png')
    plt.show()

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.locator_params(nbins=5)
    ax.plot(x, y, z)
    ax.set_title('Phase plot of v1 (V), v2 (V), i3 (mA)')
    ax.set_xlabel('v1 (V)')
    ax.set_ylabel('v2 (V)')
    ax.set_zlabel('i3 (mA)')
    fig.tight_layout()
    fig.savefig('app/ressources/export/classical_chuascircuit_phase.png')
    plt.show()

