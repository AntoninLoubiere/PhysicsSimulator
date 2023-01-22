# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>
from typing import Union

from config import G, SCALE_K, SCALE_K_SIZE, SCALE_R_ZIG_ZAG
from .abstract import ForcePoint
from points import Point, MassPoint

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


class Poids(ForcePoint):
    def __init__(self, p: Union[MassPoint, list[MassPoint]], *args, **kwargs):
        self.p = p if isinstance(p, list) else [p]
        super().__init__(self.p, *args, **kwargs)

    def get_force(self, p: MassPoint):
        return -1j * G * p.m

    def update(self):
        for p in self.p:
            p.ca += -1j * G * p.m


class Ressort(ForcePoint):
    def __init__(
            self, pta: "Point", ptb: "Point", k: float, l0: float, *args, **kwargs
    ):
        points = []
        if isinstance(pta, MassPoint):
            points.append(pta)
        elif isinstance(ptb, MassPoint):
            points.append(ptb)

        super().__init__(points, *args, **kwargs)
        self.pta = pta
        self.ptb = ptb
        self.k = k
        self.l0 = l0

        self.d_nb_points = int(SCALE_K * l0 // k) + 2

        self.d_line: Line2D

    def get_force(self, p: MassPoint):
        l = abs(self.pta.p - self.ptb.p) or 1e-10
        f = self.k * (l - self.l0) * (self.pta.p - self.ptb.p) / l
        if p == self.pta:
            return -f
        return f

    def update(self):
        l = abs(self.pta.p - self.ptb.p) or 1e-10
        f = self.k * (l - self.l0) * (self.pta.p - self.ptb.p) / l
        if isinstance(self.pta, MassPoint):
            self.pta.ca -= f
        if isinstance(self.ptb, MassPoint):
            self.ptb.ca += f

    def init_draw(self, drawables: list[Line2D]):
        (self.d_line,) = plt.plot([], [], "-", zorder=50)
        super().init_draw(drawables)
        drawables.append(self.d_line)

    def draw(self, frame_id: int):
        points = []
        t = (self.ptb.p - self.pta.p) / self.d_nb_points or 1e-10
        n = (SCALE_K_SIZE * self.k + SCALE_R_ZIG_ZAG) * t * 1j / abs(t)

        points.append(self.pta.p)
        for i in range(self.d_nb_points - 1):
            points.append((i + 0.5) * t + n + self.pta.p)
            n *= -1
        points.append(self.ptb.p)

        self.d_line.set_xdata(np.real(points))
        self.d_line.set_ydata(np.imag(points))
        super().draw(frame_id)


class FrottementsFluides(ForcePoint):
    def __init__(self, p: MassPoint, k: float, *args, **kwargs):
        super().__init__([p], *args, **kwargs)
        self.k = k
        self.p = p

    def update(self):
        self.p.ca -= self.k * self.p.v
