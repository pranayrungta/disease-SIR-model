import matplotlib.pyplot as plt
import numpy as np

def init_pop_image():
    from sir_model.plotter import _pop_image
    pop = np.random.randint(0,10,(8,8))
    Ti, Tr = 4, 10

    fig = plt.figure()
    ax = fig.add_subplot(111)
    _pop_image(ax, pop, Ti, Tr)
    fig.tight_layout()


def time_series():
    from sir_model.plotter import _timeSeriesLines
    t = np.arange(20)[...,None]
    sir = np.random.rand(20,3)
    d = np.hstack((t,sir))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    _timeSeriesLines(ax, d)
    fig.tight_layout()




def updates_data():
    pop = np.random.randint(0,10,(8,8))
    t = np.arange(20)[...,None]
    sir = np.random.rand(20,4)
    d = np.hstack((t,sir))
    return pop, d

def anim():
    from sir_model.plotter import AnimDialog
    pop = np.random.randint(0,10,(8,8))
    nbrs, Ti, Tr = 8, 4, 10

    dialog = AnimDialog(nbrs, pop, Ti, Tr)
    dialog.animate(1, 20, 0.25, updates_data)

def playPauseButton():
    from sir_model.plotter import PlayPause

    class MockAnimObj:
        def resume(self): print('resumed')
        def pause(self): print('paused')

    but = PlayPause(MockAnimObj())
    but.show()
