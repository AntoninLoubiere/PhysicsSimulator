# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

from forces import Poids, Frottements, Ressort
from points import Point, MovablePoint
from simulator import Simulation
from config import INTERVAL

A = Point(4j)
M1 = MovablePoint(
    3 + 4j,
    0,
    0.1,
)

M2 = MovablePoint(
    6 + 4j,
    -1j,
    0.2,
)

sys = Simulation(
    [A],
    [M1, M2],
    [
        Poids([M1, M2]),
        Frottements(M1, 0.0001),
        Ressort(A, M1, 5, 2),
        Ressort(M1, M2, 5, 2),
    ],
    INTERVAL,
)

# A = Point(-4)
# B = Point(-2 + 4j)
# C = Point(2 + 4j)
# D = Point(4)
# E = Point(-7.5 + 7.5j)

# M1 = MovablePoint(
#     -1 - 1j,
#     1 + 5j,
#     0.5,
# )

# M2 = MovablePoint(
#     -1 + 1j,
#     0,
#     0.1,
# )

# M3 = MovablePoint(
#     1 + 1j,
#     0,
#     0.09,
# )

# M4 = MovablePoint(
#     1 + -1j,
#     0,
#     0.1,
# )

# sim = Simulation(
#     [A, B, C, D, E],
#     [M1, M2, M3, M4],
#     [
#         Poids([M1, M2, M3, M4]),
#         Frottements(M1, 0.000000000000001),
#         Frottements(M2, 0.000000000000001),
#         Frottements(M3, 0.000000000000001),
#         Frottements(M4, 0.000000000000001),
#         Ressort(A, M1, 1, 0.5),
#         Ressort(B, M2, 1, 1),
#         Ressort(C, M3, 1, 1),
#         Ressort(D, M4, 1, 1),
#         Ressort(M1, M2, 5, 1),
#         Ressort(M2, M3, 5, 1),
#         Ressort(M3, M4, 5, 1),
#         Ressort(M4, M1, 5, 10),
#         Ressort(E, M4, 10, 5),
#         Ressort(M1, M3, 2, 3),
#         Ressort(M2, M4, 2, 3),
#     ],
#     INTERVAL,
#     100,
# )


# def randim_coord():
#     return random() * 10 - 5 + random() * 10j - 5j


# nb_points = randint(3, 10)
# nb_mov_points = randint(3, 10)
# points = [Point(randim_coord()) for _ in range(nb_points)]
# mov_points = [
#     MovablePoint(randim_coord(), randim_coord(), random() * 0.01 + 0.01)
#     for _ in range(nb_mov_points)
# ]
# # E = Point(-7.5 + 7.5j)

# forces: list[Force] = [
#     Poids(choices(mov_points, k=randint(3, nb_mov_points))),
# ]

# nb_tot = nb_points + nb_mov_points
# n = randint(5, nb_tot * 2)

# conns = set()
# while len(conns) < n:
#     a = randint(0, nb_tot - 1)
#     b = randint(0, nb_tot - 1)
#     if a != b:
#         t = tuple(sorted([a, b]))
#         if t not in conns:
#             conns.add(t)

# for p in choices(mov_points, k=randint(0, nb_mov_points)):
#     forces.append(Frottements(p, random() * 0.0000001))

# for a, b in conns:
#     pta = points[a] if a < nb_points else mov_points[a - nb_points]
#     ptb = points[b] if b < nb_points else mov_points[b - nb_points]
#     forces.append(Ressort(pta, ptb, randint(1, 10), random() * 3 + 1))

# sim = Simulation(
#     points,
#     mov_points,
#     forces,
#     INTERVAL,
#     100,
# )

# A = Point(-4j)
# B = Point(4j)
# M = MovablePoint(
#     10,
#     0,
#     0.1,
# )

# sim = Simulation(
#     [A, B],
#     [M],
#     [
#         # Poids([M]),
#         # Frottements(M, 0.0000000000000000001),
#         Ressort(A, M, 5, 5),
#         Ressort(B, M, 5, 5),
#     ],
#     INTERVAL,
#     100,
# )