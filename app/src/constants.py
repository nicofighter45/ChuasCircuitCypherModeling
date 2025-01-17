import pygame as pg
import os

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

pg.init()
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, '../ressources/Geist_Mono/GeistMono.ttf')
def get_font(size=22):
    return pg.font.Font(font_path, size)
BACKGROUND_COLOR = (235, 235, 235)

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
i3_0 = 0.1e-3

v1_0_dec = 0.02
v2_0_dec = -0.12
i3_0_dec = -0.1e-3

# simulation constants
n = 30
h = 0.4

# pre-calculated constants
a = G/C1
b = G/C2
c = 1/C1
d = -1/L
e = -Gb/C1
f = (Gb-Ga)/(2*C1)


# time constants
end = 0.02
number = 4000
