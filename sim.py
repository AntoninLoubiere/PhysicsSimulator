from random import randint, random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
from random import choices

# Simulation
A = 0 - 2j  # m
M0 = 0 + 1j  # m
V0 = 0 + 0j  # m.s^-1
L0 = 1  # m
M = 0.100  # kg
K = 0.1  #
G = 9.81  # m.s⁻²

MAX_POINTS = 40

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
time = np.linspace(0, TMPS_REEL, NB)


class Point:
    def __init__(self, p: complex, m: float = 0) -> None:
        self.p = p
        self.m = m


class MovablePoint(Point):
    def __init__(self, p0: complex, v0: complex, m: float) -> None:
        super().__init__(p0, m)
        self.v = v0

        self.ca: complex = 0

        self.init_p = p0
        self.init_v = v0

    def update(self, dt):
        self.p += self.v * dt
        self.v += self.ca * dt / self.m
        self.ca = 0

    def reset(self):
        self.p = self.init_p
        self.v = self.init_v

    def __repr__(self) -> str:
        return f"AP (p={self.p}, v={self.v}, m={self.m})"


class Force:
    def __init__(self):
        pass

    def update(self):
        raise NotImplemented

    def draw(self):
        pass

    def init_draw(self):
        return []


class ForcePoint(Force):
    def __init__(self, p: list[MovablePoint], show=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show = show
        self.points = p

        self.d_arrow: list = []

    def get_force(self, p: MovablePoint):
        return 0

    def init_draw(self):
        lst = super().init_draw()
        if self.show:
            self.d_arrow = [
                ax.arrow(
                    np.real(p.p),
                    np.imag(p.p),
                    0,
                    0,
                    color="#10b981",
                    zorder=20,
                    head_width=0.3,
                    head_length=0.3,
                )
                for p in self.points
            ]
            lst.extend(self.d_arrow)
            print(self.d_arrow)
        return lst

    def draw(self):
        for a, p in zip(self.d_arrow, self.points):
            f = self.get_force(p)
            a.set_data(x=np.real(p.p), y=np.imag(p.p), dx=np.real(f), dy=np.imag(f))
        return super().draw()


class Poids(ForcePoint):
    def __init__(self, p: MovablePoint | list[MovablePoint], *args, **kwargs):
        self.p = p if isinstance(p, list) else [p]
        super().__init__(self.p, *args, **kwargs)

    def get_force(self, p: MovablePoint):
        return -1j * G * p.m

    def update(self):
        for p in self.p:
            p.ca += -1j * G * p.m


class Ressort(ForcePoint):
    def __init__(
        self, pta: "Point", ptb: "Point", k: float, l0: float, *args, **kwargs
    ):
        points = []
        if isinstance(pta, MovablePoint):
            points.append(pta)
        elif isinstance(ptb, MovablePoint):
            points.append(ptb)

        super().__init__(points, *args, **kwargs)
        self.pta = pta
        self.ptb = ptb
        self.k = k
        self.l0 = l0

        self.d_nb_points = int(SCALE_K * l0 // k) + 2

        self.d_line: Line2D

    def get_force(self, p: MovablePoint):
        l = abs(self.pta.p - self.ptb.p) or 1e-10
        f = self.k * (l - self.l0) * (self.pta.p - self.ptb.p) / l
        if p == self.pta:
            return -f
        return f

    def update(self):
        l = abs(self.pta.p - self.ptb.p) or 1e-10
        f = self.k * (l - self.l0) * (self.pta.p - self.ptb.p) / l
        if isinstance(self.pta, MovablePoint):
            self.pta.ca -= f
        if isinstance(self.ptb, MovablePoint):
            self.ptb.ca += f

    def init_draw(self):
        (self.d_line,) = plt.plot([], [], "-", zorder=50)
        l = super().init_draw()
        l.append(self.d_line)
        return l

    def draw(self):
        points = []
        t = (self.ptb.p - self.pta.p) / self.d_nb_points
        n = (SCALE_K_SIZE * self.k + SCALE_R_ZIG_ZAG) * t * 1j / abs(t)

        points.append(self.pta.p)
        for i in range(self.d_nb_points - 1):
            points.append((i + 0.5) * t + n + self.pta.p)
            n *= -1
        points.append(self.ptb.p)

        self.d_line.set_xdata(np.real(points))
        self.d_line.set_ydata(np.imag(points))
        super().draw()


class Frottements(ForcePoint):
    def __init__(self, p: MovablePoint, k: float, *args, **kwargs):
        super().__init__([p], *args, **kwargs)
        self.k = K
        self.p = p

    def update(self):
        self.p.ca -= self.k * self.p.v


class Simulation:
    def __init__(
        self,
        points: list[Point],
        movable_points: list[MovablePoint],
        forces: list[Force],
        interval: int,
        pres: int = 10,
        chronographie: int = 5,
    ) -> None:
        self.drawables: list[Line2D] = []
        self.d_points: Line2D
        self.d_points_chrono: Line2D

        self.movable_points = movable_points
        self.points = points
        self.interval = interval
        self.dt = interval / (pres * 1000)
        self.forces = forces
        self.pres = pres

        self.chronographie = chronographie
        self.frame_id = 0
        self.chrono_p_x = []
        self.chrono_p_y = []

    def step(self):
        for f in self.forces:
            f.update()

        for p in self.movable_points:
            p.update(self.dt)

    def init(self):
        for p in self.movable_points:
            p.reset()
        self.frame_id = 0
        self.chrono_p_x = []
        self.chrono_p_y = []

    def update(self):
        for _ in range(self.pres):
            self.step()

    def __repr__(self) -> str:
        return f"Points: {self.movable_points}"

    def init_draw(self):
        (self.d_points,) = plt.plot([], [], "ro", zorder=100)
        (self.d_points_chrono,) = plt.plot([], [], "r+", zorder=100)
        points = list(p.p for p in self.points)
        plt.plot(np.real(points), np.imag(points), "o", color="black", zorder=100)

        for f in self.forces:
            self.drawables.extend(f.init_draw())
        self.drawables.append(self.d_points)
        self.drawables.append(self.d_points_chrono)

    def draw(self):
        points = list(p.p for p in self.movable_points)
        self.d_points.set_xdata(np.real(points))
        self.d_points.set_ydata(np.imag(points))

        for f in self.forces:
            f.draw()

        if self.chronographie > 0 and self.frame_id % self.chronographie == 0:
            nb_frame = self.frame_id // self.chronographie
            nb_mov_points = len(self.movable_points)
            add = len(self.chrono_p_x) < nb_mov_points * MAX_POINTS
            for i, p in enumerate(self.movable_points):
                if add:
                    self.chrono_p_x.append(np.real(p.p))
                    self.chrono_p_y.append(np.imag(p.p))
                else:
                    self.chrono_p_x[
                        (nb_frame % MAX_POINTS) * nb_mov_points + i
                    ] = np.real(p.p)
                    self.chrono_p_y[
                        (nb_frame % MAX_POINTS) * nb_mov_points + i
                    ] = np.imag(p.p)
                self.d_points_chrono.set_data(self.chrono_p_x, self.chrono_p_y)
        self.frame_id += 1

        return self.drawables


fig, ax = plt.subplots()

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

sim = Simulation(
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


sim.init_draw()


def init():
    ax.set_aspect(1.0)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    sim.init()

    return sim.draw()


def update(_):
    sim.update()
    return sim.draw()


ani = FuncAnimation(
    fig, update, frames=time, init_func=init, blit=True, interval=INTERVAL
)
plt.show()
# ani.save("anim.gif", fps=FPS)
# ani.to_html5_video()
