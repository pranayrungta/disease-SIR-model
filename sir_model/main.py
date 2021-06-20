import sir_model.plotter as pltr
from sir_model.view import UI


class Application(UI):
    def __init__(self):
        super().__init__()
        self.model = pltr.Model()
        self.initpop.generatebutton.clicked.connect(self.generatepop)
        self.initpop.plot_but.clicked.connect(lambda:
                    pltr.plotinitialpop(self.model.population)  )
        self.anim.pltSr_but.clicked.connect(self.pltSr_butfunc)
        self.anim.animate_but.clicked.connect(self.animate_butfunc)
        self.disable_plot_buttons(disable=True)

    def generatepop(self, _):
        p = self.initpop.read_parameters()
        self.model.set_pop(p['singleInfected'], p['popsize'], p['s0'])
        self.disable_plot_buttons(False)

    def set_popRange(self):
        p = self.nbrhd.get_values()
        if p['longRange']:
            self.model.set_long_range(p['nbr4'], p['p'], p['f'])
        else: self.model.set_short_range(p['nbr4'])

    def pltSr_butfunc(self, _):
        self.set_popRange()
        ti, tf, _ = self.anim.get_values()
        data = self.model.time_series_data(ti,tf)
        pltr.plot_time_series(data)

    def animate_butfunc(self, _):
        import numpy as np
        self.set_popRange()
        ti, tf, dt = self.anim.get_values()
        self.model.popRange.jumptostep(ti)
        self.model.data = np.zeros(shape=(0,6))
        anim = pltr.Population_visual( len(self.model.popRange.nbrs),
                              self.model.popRange.currentpop)
        anim.animate(ti, tf, dt, self.model.animation_data)

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
 	# main()
    pass
