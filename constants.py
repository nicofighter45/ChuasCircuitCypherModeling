WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

#Old constants
# electrical constants
C1 = 5.56e-9
C2 = 50e-9
G = 0.7e-3
L = 7.14e-3
Ga = -0.8e-3
Gb = -0.5e-3
E = 1

# initial conditions
v1_0 = -0.2
v2_0 = -0.02
i3_0 = 0.1

v1_0_dec = 0.02
v2_0_dec = -0.12
i3_0_dec = -0.1

# simulation constants
n = 30
h = 0.7



# pre-calculated constants
a = G/C1
b = G/C2
c = 1/C1
d = -1/L
e = -Gb/C1
f = (Gb-Ga)/(2*C1)



"""
# electrical constants
C1 = 10e-6
C2 = 100e-6
G = 1
L = 7e-6
Ga = -1.2
Gb = -0.8
E = 1

# initial conditions
v1_0 = 0
v2_0 = 0
i3_0 = 0

v1_0_dec = 0
v2_0_dec = 0
i3_0_dec = 0

# simulation constants
n = 10
h = 1
"""
# time constants
end = 0.02
number = 4000
