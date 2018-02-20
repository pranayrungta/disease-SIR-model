#!/usr/bin/python3.6
import plotter as pltr
import sys
from PyQt5 import QtWidgets
from ui import UI

class Application(UI):
    def __init__(self):
        super().__init__()
        self.statusbar.showMessage('Working...')

        self.singleinfected.toggled.connect(self.singleinfectedcheck)
        self.s0.valueChanged.connect(self.set1s)
        self.s0.setValue(0.45)
        self.i0.valueChanged.connect(self.set1i)
        self.r0.setDisabled(True)
        self.popsize.setValue(40)
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

        self.tstart.setValue(0)
        self.tend.setValue(50)
        self.animate_but.clicked.connect(self.animate_butfunc)
        self.animate_but.setDisabled(True)
        self.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.pltSr_but.setDisabled(True)

        self.statusbar.showMessage('Ready')

    def set1s(self):
        self.animate_but.setDisabled(True)
        self.pltSr_but.setDisabled(True)
        self.plot_but.setDisabled(True)

        self.r0.setValue(self.s0.value())
        self.i0.setValue(1-2*self.s0.value())

    def set1i(self):
        self.animate_but.setDisabled(True)
        self.pltSr_but.setDisabled(True)
        self.plot_but.setDisabled(True)

        self.s0.setValue((1-self.i0.value())/2.0)
        self.r0.setValue(self.s0.value())

    def set2s(self):
        self.plot_but.setDisabled(True)

        self.animate_but.setDisabled(True)
        self.pltSr_but.setDisabled(True)
        self.r0.setValue(1-self.s0.value())

    def singleinfectedcheck(self):
        self.statusbar.showMessage('Working...')

        if self.singleinfected.isChecked():
            self.i0.setDisabled(True)
            self.i0.valueChanged.disconnect()
            self.s0.valueChanged.disconnect()

            self.i0.setValue(0.0)
            self.s0.valueChanged.connect(self.set2s)
        else:
            self.i0.setEnabled(True)
            self.s0.valueChanged.connect(self.set1s)
            self.i0.valueChanged.connect(self.set1i)
        self.statusbar.showMessage('Ready')

    def longrangecheck(self):
        self.statusbar.showMessage('Working...')

        if self.longrange.isChecked():
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
        self.statusbar.showMessage('Ready')

    def generatepop(self):
        self.statusbar.showMessage('Working...')
        pltr.set_pop(self.singleinfected.isChecked(),
                     int(self.popsize.value()),
                     self.s0.value(),self.i0.value() )
        self.animate_but.setDisabled(False)
        self.pltSr_but.setDisabled(False)
        self.plot_but.setDisabled(False)
        self.statusbar.showMessage('Ready')

    def plottingpop(self):
        self.setDisabled(True)
        pltr.plotinitialpop()
        self.setDisabled(False)

    def set_popRange(self):
        try: p = float(self.probrewire.text())
        except ValueError: p=None
        try: f = float(self.freqrewire.text())
        except ValueError: f=None
        pltr.set_range(self.longrange.isChecked(),self.nbr4.isChecked(),p,f)
        return int(self.tstart.value()), int(self.tend.value())

    def pltSr_butfunc(self):
        self.statusbar.showMessage('Working...')
        ti, tf = self.set_popRange()
        pltr.plottimeseries(ti, tf)
        self.statusbar.showMessage('Ready')

    def animate_butfunc(self):
        self.statusbar.showMessage('Working...')
        ti, tf = self.set_popRange()
        pltr.animate(ti, tf, self.delay_spBox.value())
        self.statusbar.showMessage('Ready')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Application()
    form.show()
    sys.exit(app.exec_())
