import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

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

# Parameters
factor = 4
G = 1
C1 = 1e-1*10**(-factor)
C2 = 1*10**(-factor)
L = 7e-2*10**(-factor)
E = 1
Ga = -1.2
Gb = -0.8

# Initial conditions and time span
initial_state = [0.1, 0.0, 0.0]  # [x, y, z]
t_span = (0, 1e2*10**(-factor))
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
plt.plot(t, x, label='x(t)')
plt.plot(t, y, label='y(t)')
plt.plot(t, z, label='z(t)')
plt.title('Chua\'s Circuit Time Series')
plt.xlabel('Time')
plt.ylabel('Variables')
plt.legend()

# Phase plot (x vs z)
plt.subplot(2, 1, 2)
plt.plot(x, z, label='x vs z', color='orange')
plt.title('Phase Plot')
plt.xlabel('x')
plt.ylabel('z')
plt.legend()

plt.tight_layout()
plt.show()
