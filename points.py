# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>
from math import cos, sin
from typing import Optional

from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrow

from config import INTERVAL_S, MAX_PAST_POINTS, PAST_POINT_FRAME, SCALE_VEC_A, SCALE_VEC_V


class Point:
    movable = False
    d_points: Line2D
    d_past_points: Line2D

    def __init__(self, p: complex, m: float = 0, past_pos=True) -> None:
        self.p = p
        self.m = m

        self.past_pos_x = [] if past_pos and self.movable else None
        self.past_pos_y = [] if past_pos and self.movable else None

    def init_draw(self, drawable: list[Artist], style="o", color: Optional[str] = "black"):
        (self.d_points,) = plt.plot([self.p.real], [self.p.imag], style, color=color, zorder=100)
        if self.movable:
            drawable.append(self.d_points)
        if self.movable and self.past_pos_x is not None:
            (self.d_past_points,) = plt.plot(self.past_pos_x, self.past_pos_y, '+', color=self.d_points.get_color(),
                                             zorder=5)
            drawable.append(self.d_past_points)

    def draw(self, frame_id: int):
        self.d_points.set_data([self.p.real], [self.p.imag])
        if self.past_pos_x is not None and frame_id % PAST_POINT_FRAME == 0:
            if len(self.past_pos_x) < MAX_PAST_POINTS:
                self.past_pos_x.append(self.p.real)
                self.past_pos_y.append(self.p.imag)
            else:
                self.past_pos_x[frame_id // PAST_POINT_FRAME % MAX_PAST_POINTS] = self.p.real
                self.past_pos_y[frame_id // PAST_POINT_FRAME % MAX_PAST_POINTS] = self.p.imag

            self.d_past_points.set_data(self.past_pos_x, self.past_pos_y)

    def reset(self):
        if self.past_pos_x is not None:
            self.past_pos_x = []
            self.past_pos_y = []


class UpdatablePoint(Point):
    movable = True

    def update(self, _):
        ...


class SinusoidalPoint(UpdatablePoint):
    movable = True

    def __init__(self, center: complex, amp: complex, pulsation: float, cos_fact: complex = 1, sin_fact: complex = 1j):
        super().__init__(center)
        self.center = center
        self.amp = amp
        self.pulsation = pulsation
        self.cos_fact = cos_fact
        self.sin_fact = sin_fact

    def update(self, _):
        from simulator import Simulation
        # print(Simulation.sin.)
        self.p = self.center + self.amp * (
                self.sin_fact * sin(self.pulsation * Simulation.sim.frame_id * INTERVAL_S) +
                self.cos_fact * cos(self.pulsation * Simulation.sim.frame_id * INTERVAL_S))


class MassPoint(UpdatablePoint):
    d_v_arrow: FancyArrow
    d_a_arrow: FancyArrow

    def __init__(self, p0: complex, v0: complex, m: float, show_v_vect=False, show_a_vect=False) -> None:
        super().__init__(p0, m)
        self.v = v0

        self.a: complex = 0
        self.ca: complex = 0

        self.init_p = p0
        self.init_v = v0
        self.show_v_vect = show_v_vect
        self.show_a_vect = show_a_vect

    def init_draw(self, drawable, *args, **kwargs):
        super().init_draw(drawable, *args, **kwargs, color=None)
        if self.show_v_vect:
            v = self.v * SCALE_VEC_V
            self.d_v_arrow = plt.arrow(x=self.p.real, y=self.p.imag, dx=v.real, dy=v.imag, color="#fbbf24")
            drawable.append(self.d_v_arrow)

        if self.show_a_vect:
            a = self.a * SCALE_VEC_A
            self.d_a_arrow = plt.arrow(x=self.p.real, y=self.p.imag, dx=a.real, dy=a.imag, color="#34d399")
            drawable.append(self.d_a_arrow)

    def draw(self, frame_id: int):
        if self.show_v_vect:
            v = self.v * SCALE_VEC_V
            self.d_v_arrow.set_data(x=self.p.real, y=self.p.imag, dx=v.real, dy=v.imag)

        if self.show_a_vect:
            a = self.a * SCALE_VEC_A
            self.d_a_arrow.set_data(x=self.p.real, y=self.p.imag, dx=a.real, dy=a.imag)
        super().draw(frame_id)

    def update(self, dt):
        self.p += self.v * dt
        self.v += self.ca * dt / self.m
        self.a = self.ca
        self.ca = 0

    def reset(self):
        self.p = self.init_p
        self.v = self.init_v
        super().reset()


def __repr__(self) -> str:
    return f"AP (p={self.p}, v={self.v}, m={self.m})"
