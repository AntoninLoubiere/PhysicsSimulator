# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from points import MassPoint


class Force:
    post_update = False

    def __init__(self):
        pass

    def update(self):
        raise NotImplemented

    def draw(self, frame_id: int) -> None:
        pass

    def init_draw(self, drawables) -> None:
        return


class ForcePoint(Force):
    def __init__(self, p: list[MassPoint], show=False, *args, **kwargs):
        super().__init__()
        self.show = show
        self.points = p

        self.d_arrow: list = []

    def get_force(self, p: MassPoint):
        return 0

    def init_draw(self, drawables: list[Line2D]):
        super().init_draw(drawables)
        if self.show:
            self.d_arrow = [
                plt.arrow(
                    p.p.real,
                    p.p.imag,
                    0,
                    0,
                    color="#10b981",
                    zorder=20,
                    head_width=0.3,
                    head_length=0.3,
                )
                for p in self.points
            ]
            drawables.extend(self.d_arrow)

    def draw(self, frame_id: int):
        for a, p in zip(self.d_arrow, self.points):
            f = self.get_force(p)
            a.set_data(x=p.p.real, y=p.p.imag, dx=f.real, dy=f.imag)
        return super().draw(frame_id)
