# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

from itertools import chain

from matplotlib.lines import Line2D

from forces.abstract import Force
from points import Point, UpdatablePoint


class Simulation:
    sim: "Simulation" = None

    def __init__(
            self,
            points: list[Point],
            updatable_points: list[UpdatablePoint],
            forces: list[Force],
            interval: int,
            pres: int = 10,
    ) -> None:
        Simulation.sim = self
        self.drawables: list[Line2D] = []

        self.movable_points = updatable_points
        self.points = points
        self.interval = interval
        self.dt = interval / (pres * 1000)
        self.forces = forces
        self.pres = pres

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
        for f in self.forces:
            f.init_draw(self.drawables)

        for p in chain(self.points, self.movable_points):
            p.init_draw(self.drawables)

        return self.drawables

    def draw(self):
        for f in self.forces:
            f.draw(self.frame_id)

        for p in self.movable_points:
            p.draw(self.frame_id)
        self.frame_id += 1

        # if self.chronographie > 0 and self.frame_id % self.chronographie == 0:
        #     nb_frame = self.frame_id // self.chronographie
        #     nb_mov_points = len(self.movable_points)
        #     add = len(self.chrono_p_x) < nb_mov_points * MAX_POINTS
        #     for i, p in enumerate(self.movable_points):
        #         if add:
        #             self.chrono_p_x.append(p.p.real)
        #             self.chrono_p_y.append(p.p.imag)
        #         else:
        #             self.chrono_p_x[
        #                 (nb_frame % MAX_POINTS) * nb_mov_points + i
        #                 ] = p.p.real
        #             self.chrono_p_y[
        #                 (nb_frame % MAX_POINTS) * nb_mov_points + i
        #                 ] = p.p.imag
        #         self.d_points_chrono.set_data(self.chrono_p_x, self.chrono_p_y)
        # self.frame_id += 1

        return self.drawables
