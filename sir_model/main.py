import sir_model.plotter as pltr
from sir_model.view import UI


class Application(UI):
    def __init__(self):
        super().__init__()
        self.initpop.generatebutton.clicked.connect(self.generatepop)
        self.initpop.plot_but.clicked.connect(pltr.plotinitialpop)
        self.anim.animate_but.clicked.connect(self.animate_butfunc)
        self.anim.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.disable_plot_buttons(disable=True)

    def generatepop(self, _):
        p = self.initpop.read_parameters()
        pltr.set_pop(p['singleInfected'], p['popsize'], p['s0'])
        self.disable_plot_buttons(False)

    def set_popRange(self):
        p = self.nbrhd.get_values()
        if p['longRange']:
            pltr.set_long_range(p['nbr4'], p['p'], p['f'])
        else: pltr.set_short_range(self.nbrhd.nbr4.isChecked())

    def pltSr_butfunc(self, _):
        self.set_popRange()
        ti, tf, _ = self.anim.get_values()
        pltr.plot_time_series(ti, tf)

    def animate_butfunc(self, _):
        self.set_popRange()
        ti, tf, dt = self.anim.get_values()
        pltr.animate(ti, tf, dt)


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
	main()
