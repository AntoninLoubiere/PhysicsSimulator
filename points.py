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