import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config import TMPS_REEL, NB, INTERVAL
from system import sys

time = np.linspace(0, TMPS_REEL, NB)

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
    fig, update, frames=time, init_func=init, blit=True, interval=INTERVAL
)
plt.show()
# ani.save("anim.gif", fps=FPS)
# ani.to_html5_video()
