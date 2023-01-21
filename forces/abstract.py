# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

from points import MovablePoint
import matplotlib.pyplot as plt

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
            lst.extend(self.d_arrow)
            print(self.d_arrow)
        return lst

    def draw(self):
        for a, p in zip(self.d_arrow, self.points):
            f = self.get_force(p)
            a.set_data(x=p.p.real, y=p.p.imag, dx=f.real, dy=f.imag)
        return super().draw()