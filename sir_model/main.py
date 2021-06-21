import sir_model.plotter as plt
from sir_model.controls import Controls
from sir_model.model import Model

class Application:
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.ui = Controls()
        self.ui.initpop.generatebutton.clicked.connect(self.generatepop)
        self.ui.initpop.plot_but.clicked.connect(self.plt_initpop)
        self.ui.anim.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.ui.anim.animate_but.clicked.connect(self.animate_butfunc)

    def generatepop(self, _):
        p = self.ui.initpop.get_values()
        self.model.set_pop(p['singleInfected'], p['popsize'], p['s0'])
        self.ui.disable_plot_buttons(False)

    def plt_initpop(self, _):
        pop, census, Ti, Tr = self.model.init_pop()
        plt.plotinitialpop(pop, census, Ti, Tr)

    def pltSr_butfunc(self, _):
        p = self.ui.nbrhd.get_values()
        self.model.set_popRange(p)
        ti, tf, _ = self.ui.anim.get_values()
        data = self.model.time_series_data(ti,tf)
        plt.plot_time_series(data)

    def animate_butfunc(self, _):
        p = self.ui.nbrhd.get_values()
        self.model.set_popRange(p)
        ti, tf, dt = self.ui.anim.get_values()
        nbrs, pop, Ti, Tr, updater = self.model.get_anim_updater(ti)
        anim = plt.Population_visual(nbrs, pop, Ti, Tr)
        anim.animate(ti, tf, dt, updater)

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
 	# main()
    form = Application()
    form.ui.show()
    pass
