import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
sys.path.append("../")
from app.src.constants import *



# Chua's circuit equations
def chua_circuit(_, state):
    x, y, z = state
    # Nonlinear term
    f_x = Gb * x + (Ga - Gb) * (np.abs(x + E) - np.abs(x - E)) / 2
    # ODEs
    dxdt = 1/C1 * (G*(y - x) - f_x)
    dydt = 1/C2*(G*(x - y) + z)
    dzdt = -y /L
    return [dxdt, dydt, dzdt]

# Initial conditions and time span
initial_state = [0.1, 0.0, 0.0]  # [x, y, z]
t_span = (0, 1e-2)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

# Solve the system
solution = solve_ivp(
    chua_circuit,
    t_span,
    initial_state,
    t_eval=t_eval,
    method='RK45'
)

# Extract results
t = solution.t
x, y, z = solution.y

# Plot the results
fig = plt.figure(figsize=(12, 8))

# Time series
plt.subplot(2, 1, 1)
plt.plot(t, x, label='v1 (V)')
plt.plot(t, y, label='v2 (V)')
plt.plot(t, z, label='i3 (mA)')
plt.title("Classical Chua's circuit with the study's values")
plt.xlabel('Time (s)')
plt.ylabel('U (V)')
plt.legend()

# Phase plot (x vs z)
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Phase plot (x, y, z)', color='orange')
ax.set_title('3D Phase Plot')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Add legend
ax.legend()

plt.tight_layout()
plt.show()
