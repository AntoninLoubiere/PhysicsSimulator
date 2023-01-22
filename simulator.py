# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

from itertools import chain
from typing import Optional

from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.backend_bases import MouseButton, MouseEvent

from config import INTERVAL, SELECT_RADIUS, VITESSE_ANIM
from forces.abstract import Force
from points import MassPoint, Point, UpdatablePoint


class Simulation:
    sim: "Simulation" = None

    def __init__(
            self,
            points: list[Point] = None,
            forces: list[Force] = None,
            pres: int = 50,
            interval: int = INTERVAL * VITESSE_ANIM / 100,
    ) -> None:
        Simulation.sim = self
        self.drawables: list[Artist] = []

        self.updatable_points = []
        self.points = []
        if points is not None:
            for p in points:
                if isinstance(p, UpdatablePoint):
                    self.updatable_points.append(p)
                else:
                    self.points.append(p)

        self.interval = interval
        self.dt = interval / (pres * 1000)

        self.forces = []
        self.post_update_force = []
        if forces:
            for f in forces:
                if f.post_update:
                    self.post_update_force.append(f)
                else:
                    self.forces.append(f)

        self.pres = pres

        self.frame_id = 0
        self.chrono_p_x = []
        self.chrono_p_y = []

        self.selected: Optional[Point] = None
        self.selected_is_not_updatable = False
        self.select_event_id = -1
        self.mouse_pos: complex = 0
        self.mouse_last_pos: complex = 0

    def step(self):
        for f in self.forces:
            f.update()

        for f in self.post_update_force:
            f.update()

        if self.selected is not None:
            self.selected.on_select_move(self.mouse_pos)
            if isinstance(self.selected, MassPoint):
                self.selected.v = 0
                self.selected.ca = 0

        for p in self.updatable_points:
            p.update(self.dt)

    def init(self):
        for p in self.updatable_points:
            p.reset()
        self.frame_id = 0
        self.chrono_p_x = []
        self.chrono_p_y = []

    def update(self):
        for _ in range(self.pres):
            self.step()

    def __repr__(self) -> str:
        return f"Points: {self.updatable_points}"

    def on_move(self, event: MouseEvent):
        if event.button is MouseButton.LEFT:
            if event.inaxes:
                self.mouse_last_pos = self.mouse_pos
                self.mouse_pos = complex(event.xdata, event.ydata)
        else:
            event.button = MouseButton.LEFT
            self.on_release(event)

    def on_press(self, event: MouseEvent):
        if event.button is MouseButton.LEFT and event.inaxes:
            c = complex(event.xdata, event.ydata)
            min_non_updatable = min(self.points, key=lambda p: abs(c - p.p), default=None)
            min_updatable = min(self.updatable_points, key=lambda p: abs(c - p.p), default=None)
            point = min((min_updatable, min_non_updatable), key=lambda p: abs(c - p.p), default=None)
            if point is not None and abs(c - point.p) < SELECT_RADIUS:
                self.selected = point
                self.mouse_pos = c
                self.mouse_last_pos = c
                self.selected_is_not_updatable = point == min_non_updatable
                self.select_event_id = plt.connect('motion_notify_event', self.on_move)

    def on_release(self, event: MouseEvent):
        if event.button is MouseButton.LEFT and self.selected is not None:
            if isinstance(self.selected, MassPoint):
                c = complex(event.xdata, event.ydata) if event.inaxes else self.mouse_pos
                self.selected.v = (c - self.mouse_last_pos) / (self.dt * self.pres)
            self.selected = None
            self.selected_is_not_updatable = False
            plt.disconnect(self.select_event_id)

    def init_draw(self):
        for f in self.forces:
            f.init_draw(self.drawables)

        for p in chain(self.points, self.updatable_points):
            p.init_draw(self.drawables)

        plt.connect('button_press_event', self.on_press)
        plt.connect('button_release_event', self.on_release)

        return self.drawables

    def draw(self):
        for f in self.forces:
            f.draw(self.frame_id)

        for p in self.updatable_points:
            p.draw(self.frame_id)

        if self.selected_is_not_updatable:
            self.selected.draw(self.frame_id)

        self.frame_id += 1
        return self.drawables
