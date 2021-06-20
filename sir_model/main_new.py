from . import plotter as pltr
from .ui import UInew
import functools

def responsive_action(action):
    @functools.wraps(action)
    def wrapper(app, *args, **kwargs):
        app.statusbar.showMessage('Working...')
        action(app, *args, **kwargs)
        app.statusbar.showMessage('Ready')
    return wrapper


class Application:
    def __init__(self):
        self.ui = UInew()

    def disable_plot_buttons(self, disable=True):
        self.animate_but.setDisabled(disable)
        self.pltSr_but.setDisabled(disable)
        self.plot_but.setDisabled(disable)


    @responsive_action
    def generatepop(self, _):
        pltr.set_pop(self.singleinfected.isChecked(),
                     int(self.popsize.value()),
                     self.s0.value() )
        self.disable_plot_buttons(False)

    def set_popRange(self):
        if self.longrange.isChecked():
            try: p = float(self.probrewire.text())
            except ValueError: p=0.1
            try: f = float(self.freqrewire.text())
            except ValueError: f=10
            pltr.set_long_range(self.nbr4.isChecked(), p, f)
        else: pltr.set_short_range(self.nbr4.isChecked())

    @responsive_action
    def pltSr_butfunc(self, _):
        self.set_popRange()
        ti, tf = int(self.tstart.value()), int(self.tend.value())
        pltr.plot_time_series(ti, tf)

    @responsive_action
    def animate_butfunc(self, _):
        self.set_popRange()
        ti, tf = int(self.tstart.value()), int(self.tend.value())
        pltr.animate(ti, tf, self.delay_spBox.value())


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
	main()
