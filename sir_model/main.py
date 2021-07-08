import sir_model.plotter as plt
from sir_model.controls import Controls
from sir_model.model import Model


class Application:
    def __init__(self):
        self.model = Model()
        self.ui = Controls()
        self.ui.initpop.generatebutton.clicked.connect(self.generate_pop)
        self.ui.initpop.plot_but.clicked.connect(self.plt_initpop)
        self.ui.anim.pltSr_but.clicked.connect(self.plt_series)
        self.ui.anim.animate_but.clicked.connect(self.plt_animation)

    def generate_pop(self, _):
        self.ui.status('Working...')
        p = self.ui.initpop.get_values()
        self.model.set_pop(p)
        self.ui.disable_plot_buttons(False)
        self.ui.status('Ready')

    def plt_initpop(self, _):
        self.ui.status('Working...')
        pop, census, Ti, Tr = self.model.init_pop()
        self.ip_dialog = plt.plotInitialPop(pop, census, Ti, Tr)
        self.ui.status('Ready')

    def plt_series(self, _):
        self.ui.status('Working...')
        p = self.ui.nbrhd.get_values()
        ti, tf, _ = self.ui.anim.get_values()
        self.model.set_popRange(p)
        data = self.model.time_series_data(ti,tf)
        self.ts_dialog = plt.plotTimeSeries(data)
        self.ui.status('Ready')

    def plt_animation(self, _):
        self.ui.status('Working...')
        p = self.ui.nbrhd.get_values()
        ti, tf, dt = self.ui.anim.get_values()
        self.model.set_popRange(p)
        nbrs, pop, Ti, Tr, updater = self.model.get_anim_updater(ti)
        self.anim_dialog = plt.AnimDialog(nbrs, pop, Ti, Tr)
        self.anim_dialog.animate(ti, tf, dt, updater)
        self.ui.status('Ready')

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = Application()
    form.ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    form = Application()
    form.ui.show()
