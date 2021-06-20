import sir_model.plotter as pltr
from sir_model.view import UI


class Application(UI):
    def __init__(self):
        super().__init__()
        self.initpop.generatebutton.clicked.connect(self.generatepop)
        self.anim.animate_but.clicked.connect(self.animate_butfunc)
        self.anim.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.initpop.plot_but.clicked.connect(pltr.plotinitialpop)
        self.disable_plot_buttons(disable=True)

    def generatepop(self, _):
        pltr.set_pop(self.initpop.singleinfected.isChecked(),
                     int(self.initpop.popsize.value()),
                     self.initpop.s0.value() )
        self.disable_plot_buttons(False)

    def set_popRange(self):
        if self.nbrhd.longrange.isChecked():
            try: p = float(self.nbrhd.probrewire.text())
            except ValueError: p=0.1
            try: f = float(self.nbrhd.freqrewire.text())
            except ValueError: f=10
            pltr.set_long_range(self.nbrhd.nbr4.isChecked(), p, f)
        else: pltr.set_short_range(self.nbrhd.nbr4.isChecked())

    def pltSr_butfunc(self, _):
        self.set_popRange()
        ti = int(self.anim.tstart.value())
        tf = int(self.anim.tend.value())
        pltr.plot_time_series(ti, tf)

    def animate_butfunc(self, _):
        self.set_popRange()
        ti = int(self.anim.tstart.value())
        tf = int(self.anim.tend.value())
        pltr.animate(ti, tf, self.anim.delay_spBox.value())


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
	main()
