from cmath import phase

from sympy import Line2D

from forces.abstract import CurveRestriction
from points import MassPoint, Point


class CircleRestriction(CurveRestriction):
    d_line: Line2D
    def __init__(self, center: Point, p: list[MassPoint], radius: int, *args, **kwargs):
        super().__init__(p, *args, **kwargs)
        self.center = center
        self.radius = radius

    def update(self) -> None:
        for p in self.points:
            rel_p = (self.center.p - p.p)
            rel_p_abs = abs(rel_p)
            if rel_p_abs >= self.radius:
                reac = self.apply_reaction(p, rel_p, self.radius)
                p.p = self.center.p - self.radius * rel_p / abs(rel_p)

                if isinstance(self.center, MassPoint):
                    self.center.ca -= reac


    def init_draw(self, drawables: list[Line2D]):
        super().init_draw(drawables)
    def draw(self, frame_id: int):
        pass
