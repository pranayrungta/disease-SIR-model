import PyQt5.QtWidgets as qt
from PyQt5.QtCore import pyqtSignal

def set_icon(win):
    from pathlib import Path
    from PyQt5.QtGui import QIcon
    icon = str(Path(__file__).parent/"icon.png")
    win.setWindowIcon(QIcon(icon))

def DoubleSpinBox(minimum=0, maximum=1.0, singleStep=0.1):
    box = qt.QDoubleSpinBox()
    box.setMinimum(minimum)
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
    return box

def SpinBox(maximum, singleStep, init_value=0):
    box = qt.QSpinBox()
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
    box.setProperty("value", init_value)
    return box

def FormLay(label_Field_list:dict):
    formLayout = qt.QFormLayout()
    for label,field in label_Field_list.items():
        formLayout.addRow(qt.QLabel(label), field)
    return formLayout


class Initpop(qt.QGroupBox):
    newValueSelected = pyqtSignal()
    def __init__(self):
        super().__init__("Initial Population")
        self.singleinfected = qt.QCheckBox("Single Infected Individual")
        self.s0 = DoubleSpinBox()
        self.i0 = DoubleSpinBox()
        self.r0 = DoubleSpinBox()
        self.popsize = SpinBox(200, 10)
        self.generatebutton = qt.QPushButton("Generate")
        self.plot_but = qt.QPushButton("Plot")

        self._set_all_layouts()
        self._make_connections()

    def get_values(self):
        return {'singleInfected' : self.singleinfected.isChecked(),
                'popsize' : self.popsize.value(),
                's0': self.s0.value()}

    def _make_connections(self):
        self.r0.setDisabled(True)
        self.popsize.setValue(40)
        self.plot_but.setDisabled(True)
        self.singleinfected.toggled.connect(self._value_changed)
        self.s0.valueChanged.connect(self._value_changed)
        self.i0.valueChanged.connect(self._value_changed)
        self.popsize.valueChanged.connect(self.newValueSelected.emit)
        self.s0.setValue(0.45)

    def _value_changed(self):
        for i in [self.s0, self.i0, self.r0]:
            i.blockSignals(True)
        if self.singleinfected.isChecked():
            self.i0.setDisabled(True)
            self.s0.setMaximum(1)
            self.i0.setValue(0.0)
            self.r0.setValue(1-self.s0.value())
        else:
            self.i0.setEnabled(True)
            if self.sender() is self.s0:
                self.s0.setMaximum(0.5)
                self.i0.setValue(1-2*self.s0.value())
                self.r0.setValue(self.s0.value())
            else:
                self.s0.setMaximum(1)
                val = (1-self.i0.value())/2.0
                self.s0.setValue(val)
                self.r0.setValue(val)
        for i in [self.s0, self.i0, self.r0]:
            i.blockSignals(False)
        self.newValueSelected.emit()

    def _set_all_layouts(self):
        vLayout = qt.QVBoxLayout()
        vLayout.addWidget(self.singleinfected)
        vLayout.addLayout(FormLay({"So:" : self.s0,
                                   "Io:" : self.i0,
                                   "Ro:" : self.r0,
                                   "Size:" : self.popsize}))
        vLayout.addStretch()
        vLayout.addWidget(self.generatebutton)
        vLayout.addWidget(self.plot_but)
        self.setLayout(vLayout)


class Neighbourhood(qt.QGroupBox):
    def __init__(self):
        super().__init__("Neighbourhood")
        self.nbr4 = qt.QRadioButton("von Neumann(4)")
        self.nbr4.setChecked(True)
        self.nbr8 = qt.QRadioButton("Moore(8)")
        self.longrange = qt.QCheckBox("Long Range Interactions")
        self.probrewire = qt.QLineEdit()
        self.freqrewire = qt.QLineEdit()
        self._set_all_layouts()

    def get_values(self):
        lr =  self.longrange.isChecked()
        nbr4 = self.nbr4.isChecked()
        vals = {'longRange':lr, 'nbr4': nbr4}
        if lr:
            try:
                p = float(self.probrewire.text())
                if p<0 or p>1: raise ValueError
            except ValueError: p=0.1
            try: f = int(self.freqrewire.text())
            except ValueError: f=10
            self.probrewire.setText(str(p))
            self.freqrewire.setText(str(f))
            vals.update({'p':p, 'f':f})
        return vals

    def _set_all_layouts(self):
        vLayout = qt.QVBoxLayout()
        vLayout.addWidget(self.nbr4)
        vLayout.addWidget(self.nbr8)
        vLayout.addWidget(self.longrange)
        vLayout.addStretch()
        frame = qt.QFrame()
        frame.setLayout(FormLay({
            "Probability:" : self.probrewire,
            "Frequency:" : self.freqrewire}) )
        frame.setVisible(False)
        self.longrange.toggled.connect(frame.setVisible)
        vLayout.addWidget(frame)
        self.setLayout(vLayout)


class Animate(qt.QGroupBox):
    def __init__(self):
        super().__init__("Animate")
        self.tstart = SpinBox(10000,10)
        self.tend = SpinBox(100000,10)
        self.delay_spBox = DoubleSpinBox(0.05, 5.0, 0.5)
        self.animate_but = qt.QPushButton("Animate!")
        self.pltSr_but = qt.QPushButton("Plot Time Series")
        self._set_all_layouts()

    def get_values(self):
        return (int(self.tstart.value()),
                int(self.tend.value()),
                self.delay_spBox.value() )

    def _set_all_layouts(self):
        self.tstart.setValue(0)
        self.tend.setValue(50)
        self.delay_spBox.setValue(0.2)
        vLayout = qt.QVBoxLayout()
        vLayout.addLayout(FormLay({"Start time"  : self.tstart,
                                   "End time"    : self.tend,
                                   "Delay(secs)" : self.delay_spBox}) )
        vLayout.addStretch()
        vLayout.addWidget(self.animate_but)
        vLayout.addWidget(self.pltSr_but)
        self.setLayout(vLayout)


class Controls(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initpop = Initpop()
        self.nbrhd = Neighbourhood()
        self.anim = Animate()
        self._set_all_layouts()
        self.initpop.newValueSelected.connect(self.disable_plot_buttons)
        self.disable_plot_buttons()

    def disable_plot_buttons(self, disable=True):
        self.anim.animate_but.setDisabled(disable)
        self.anim.pltSr_but.setDisabled(disable)
        self.initpop.plot_but.setDisabled(disable)

    def _set_all_layouts(self):
        self.setWindowTitle("S I R Model")
        set_icon(self)
        centralwidget = qt.QWidget(self)
        self.setCentralWidget(centralwidget)
        horizontalLayout = qt.QHBoxLayout(centralwidget)
        horizontalLayout.addWidget(self.initpop)
        horizontalLayout.addStretch()
        horizontalLayout.addWidget(self.nbrhd)
        horizontalLayout.addStretch()
        horizontalLayout.addWidget(self.anim)
        self.statusbar = qt.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')

    def status(self, msg='Ready'):
        self.statusbar.showMessage(msg)
        self.repaint()

if __name__ == '__main__':
    form = Controls()
    form.show()
