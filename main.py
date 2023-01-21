# PhysicsSimulator Copyright (C) 2023 Antonin LOUBIERE
# License GPL-3 <https://www.gnu.org/licenses/gpl-3.0.html>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from config import INTERVAL, NB
from system import sys

fig, ax = plt.subplots()


sys.init_draw()


def init():
    ax.set_aspect(1.0)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    sys.init()
    return sys.draw()


def update(_):
    sys.update()
    return sys.draw()


ani = FuncAnimation(
    fig, update, frames=NB, init_func=init, blit=True, interval=INTERVAL
)
plt.show()
# ani.save("anim.gif", fps=FPS)
# ani.to_html5_video()
