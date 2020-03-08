#!/usr/bin/python3.6
from . import plotter as pltr
from .ui import UI
import functools

def responsive_action(action):
    @functools.wraps(action)
    def wrapper(app, *args, **kwargs):
        app.statusbar.showMessage('Working...')
        action(app, *args, **kwargs)
        app.statusbar.showMessage('Ready')
    return wrapper


class Application(UI):
    def __init__(self):
        super().__init__()
        self.statusbar.showMessage('Working...')

        self.s0.setValue(0.45)
        self.r0.setDisabled(True)
        self.popsize.setValue(40)
        self.longrangecheck(False)
        self.tstart.setValue(0)
        self.tend.setValue(50)
        self.disable_plot_buttons()

        self.singleinfected.toggled.connect(self.singleinfectedcheck)
        self.s0.valueChanged.connect(self.set_sus_changed)
        self.i0.valueChanged.connect(self.set_inf_changed)
        self.popsize.valueChanged.connect(self.disable_plot_buttons)
        self.generatebutton.clicked.connect(self.generatepop)
        self.longrange.toggled.connect(self.longrangecheck)
        self.plot_but.clicked.connect(pltr.plotinitialpop)
        self.animate_but.clicked.connect(self.animate_butfunc)
        self.pltSr_but.clicked.connect(self.pltSr_butfunc)

        self.statusbar.showMessage('Ready')

    @responsive_action
    def singleinfectedcheck(self, checked):
        if checked:
            self.i0.setValue(0.0)
            self.i0.setDisabled(True)
            self.s0.valueChanged.connect(self.set_single_inf_values)
        else:
            self.i0.setEnabled(True)
            self.s0.valueChanged.connect(self.set_sus_changed)

    def disable_plot_buttons(self, disable=True):
        self.animate_but.setDisabled(disable)
        self.pltSr_but.setDisabled(disable)
        self.plot_but.setDisabled(disable)

    def set_sus_changed(self):
        self.disable_plot_buttons()
        self.r0.setValue(self.s0.value())
        self.i0.setValue(1-2*self.s0.value())

    def set_inf_changed(self):
        self.disable_plot_buttons()
        self.s0.setValue((1-self.i0.value())/2.0)
        self.r0.setValue(self.s0.value())

    def set_single_inf_values(self):
        self.disable_plot_buttons()
        self.r0.setValue(1-self.s0.value())

    @responsive_action
    def longrangecheck(self, checked):
        if checked:
            self.probrewire.setDisabled(False)
            self.probrewire.show()
            self.prob_label.show()
            self.freqrewire.setDisabled(False)
            self.freqrewire.show()
            self.freq_label.show()
        else:
            self.probrewire.setDisabled(True)
            self.probrewire.hide()
            self.prob_label.hide()
            self.freqrewire.setDisabled(True)
            self.freqrewire.hide()
            self.freq_label.hide()

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
