# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

# Simulation
A = 0 - 2j  # m
M0 = 0 + 1j  # m
V0 = 0 + 0j  # m.s^-1
L0 = 1  # m
M = 0.100  # kg
K = 0.1  #
G = 9.81  # m.s⁻²


TMPS_REEL = 20  # s
VITESSE_ANIM = 100  # %
FPS = 60  # NE PAS DÉPASSER 60

SCALE_K = 20
SCALE_R_ZIG_ZAG = 0.1
SCALE_K_SIZE = 0.01

SCALE_VEC = 0.01

# Constantes
INTERVAL = 1000 // FPS
NB = 100 * TMPS_REEL * FPS // VITESSE_ANIM

PAST_POINT_FRAME = 2
MAX_PAST_POINTS = FPS // PAST_POINT_FRAME
