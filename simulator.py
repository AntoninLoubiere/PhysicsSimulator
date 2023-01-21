# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

from config import MAX_POINTS
from forces.abstract import Force
from points import MovablePoint, Point

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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
                    self.chrono_p_x.append(p.p.real)
                    self.chrono_p_y.append(p.p.imag)
                else:
                    self.chrono_p_x[
                        (nb_frame % MAX_POINTS) * nb_mov_points + i
                    ] = p.p.real
                    self.chrono_p_y[
                        (nb_frame % MAX_POINTS) * nb_mov_points + i
                    ] = p.p.imag
                self.d_points_chrono.set_data(self.chrono_p_x, self.chrono_p_y)
        self.frame_id += 1

        return self.drawables