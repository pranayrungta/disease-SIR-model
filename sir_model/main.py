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
        self.popsize.setValue(40)
        self.tstart.setValue(0)
        self.tend.setValue(50)

        self.singleinfected.toggled.connect(self.singleinfectedcheck)
        self.s0.valueChanged.connect(self.set1s)
        self.i0.valueChanged.connect(self.set1i)
        self.r0.setDisabled(True)

        self.generatebutton.clicked.connect(self.generatepop)
        self.plot_but.clicked.connect(self.plottingpop)
        self.plot_but.setDisabled(True)

        self.longrange.toggled.connect(self.longrangecheck)
        self.probrewire.setDisabled(True)
        self.probrewire.hide()
        self.prob_label.hide()
        self.freqrewire.setDisabled(True)
        self.freqrewire.hide()
        self.freq_label.hide()

        self.animate_but.clicked.connect(self.animate_butfunc)
        self.animate_but.setDisabled(True)
        self.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.pltSr_but.setDisabled(True)

        self.statusbar.showMessage('Ready')

    def disable_plot_buttons(self):
        self.animate_but.setDisabled(True)
        self.pltSr_but.setDisabled(True)
        self.plot_but.setDisabled(True)

    def set1s(self):
        self.disable_plot_buttons()
        self.r0.setValue(self.s0.value())
        self.i0.setValue(1-2*self.s0.value())

    def set1i(self):
        self.disable_plot_buttons()
        self.s0.setValue((1-self.i0.value())/2.0)
        self.r0.setValue(self.s0.value())

    def set_single_inf_values(self):
        self.disable_plot_buttons()
        self.r0.setValue(1-self.s0.value())

    @responsive_action
    def singleinfectedcheck(self, checked):
        if checked:
            self.i0.setValue(0.0)
            self.i0.setDisabled(True)
            self.s0.valueChanged.disconnect()
            self.s0.valueChanged.connect(self.set_single_inf_values)
        else:
            self.i0.setEnabled(True)
            self.s0.valueChanged.connect(self.set1s)

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
                     self.s0.value(),self.i0.value() )
        self.animate_but.setDisabled(False)
        self.pltSr_but.setDisabled(False)
        self.plot_but.setDisabled(False)

    def set_popRange(self):
        try: p = float(self.probrewire.text())
        except ValueError: p=None
        try: f = float(self.freqrewire.text())
        except ValueError: f=None
        pltr.set_range(self.longrange.isChecked(),self.nbr4.isChecked(),p,f)
        return int(self.tstart.value()), int(self.tend.value())

    @responsive_action
    def plottingpop(self, _):
        pltr.plotinitialpop()

    @responsive_action
    def pltSr_butfunc(self, _):
        ti, tf = self.set_popRange()
        pltr.plottimeseries(ti, tf)

    @responsive_action
    def animate_butfunc(self, _):
        ti, tf = self.set_popRange()
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
