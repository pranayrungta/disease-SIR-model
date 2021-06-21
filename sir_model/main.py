import sir_model.plotter as pltr
from sir_model.view import Controls
from sir_model.model import Model

class Application:
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.ui = Controls()
        self.ui.initpop.generatebutton.clicked.connect(self.generatepop)
        self.ui.initpop.plot_but.clicked.connect(lambda:
                    pltr.plotinitialpop(self.model.population)  )
        self.ui.anim.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.ui.anim.animate_but.clicked.connect(self.animate_butfunc)
        self.ui.disable_plot_buttons(disable=True)

    def generatepop(self, _):
        p = self.ui.initpop.get_values()
        self.model.set_pop(p['singleInfected'], p['popsize'], p['s0'])
        self.ui.disable_plot_buttons(False)

    def pltSr_butfunc(self, _):
        # self.set_popRange()
        p = self.ui.nbrhd.get_values()
        self.model.set_popRange(p)
        ti, tf, _ = self.ui.anim.get_values()
        data = self.model.time_series_data(ti,tf)
        pltr.plot_time_series(data)

    def animate_butfunc(self, _):
        # self.set_popRange()
        p = self.ui.nbrhd.get_values()
        self.model.set_popRange(p)
        ti, tf, dt = self.ui.anim.get_values()
        nbrs, pop, updater = self.model.get_anim_updater(ti)
        anim = pltr.Population_visual(nbrs, pop)
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
