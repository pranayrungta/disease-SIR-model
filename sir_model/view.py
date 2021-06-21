from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

def DoubleSpinBox(minimum=0, maximum=1.0, singleStep=0.1):
    box = QtWidgets.QDoubleSpinBox()
    box.setMinimum(minimum)
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
    return box

def SpinBox(maximum, singleStep, init_value=0):
    box = QtWidgets.QSpinBox()
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
    box.setProperty("value", init_value)
    return box

def FormLay(label_Field_list):
    formLayout = QtWidgets.QFormLayout()
    for i,(label,field) in enumerate(label_Field_list):
        formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, label)
        formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, field)
    return formLayout


class Initpop(QtWidgets.QWidget):
    newValueSelected = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.singleinfected = QtWidgets.QCheckBox("Single Infected Individual")
        self.s0 = DoubleSpinBox()
        self.i0 = DoubleSpinBox()
        self.r0 = DoubleSpinBox()
        self.popsize = SpinBox(200, 10)
        self.generatebutton = QtWidgets.QPushButton("Generate")
        self.plot_but = QtWidgets.QPushButton("Plot")

        self.set_all_layouts()
        self.make_connections()

    def get_values(self):
        return {'singleInfected' : self.singleinfected.isChecked(),
                'popsize' : self.popsize.value(),
                's0': self.s0.value()}

    def make_connections(self):
        self.r0.setDisabled(True)
        self.popsize.setValue(40)
        self.plot_but.setDisabled(True)
        self.singleinfected.toggled.connect(self.value_changed)
        self.s0.valueChanged.connect(self.value_changed)
        self.i0.valueChanged.connect(self.value_changed)
        self.popsize.valueChanged.connect(self.newValueSelected.emit)
        self.s0.setValue(0.45)

    def value_changed(self):
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

    def set_all_layouts(self):
        s0_label = QtWidgets.QLabel("So:")
        i0_label = QtWidgets.QLabel("Io:")
        r0_label = QtWidgets.QLabel("Ro:")
        size_label = QtWidgets.QLabel("Size:")
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(self.singleinfected)
        vLayout.addLayout(FormLay([[s0_label,   self.s0],
                                   [i0_label,   self.i0],
                                   [r0_label,   self.r0],
                                   [size_label, self.popsize]]))
        vLayout.addStretch()
        vLayout.addWidget(self.generatebutton)
        vLayout.addWidget(self.plot_but)
        grpBox = QtWidgets.QGroupBox("Initial Population")
        grpBox.setLayout(vLayout)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(grpBox)
        self.setLayout(layout)



class Neighbourhood(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.nbr4 = QtWidgets.QRadioButton("von Neumann(4)")
        self.nbr4.setChecked(True)
        self.nbr8 = QtWidgets.QRadioButton("Moore(8)")
        self.longrange = QtWidgets.QCheckBox("Long Range Interactions")
        self.prob_label = QtWidgets.QLabel("Probability:")
        self.probrewire = QtWidgets.QLineEdit()
        self.freq_label = QtWidgets.QLabel("Frequency:")
        self.freqrewire = QtWidgets.QLineEdit()
        self.set_all_layouts()
        self.longrange.toggled.connect(self.longrangecheck)

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

    def longrangecheck(self, checked):
        for i in [self.prob_label, self.probrewire,
                  self.freq_label, self.freqrewire]:
            i.setVisible(checked)

    def set_all_layouts(self):
        self.longrangecheck(False)
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(self.nbr4)
        vLayout.addWidget(self.nbr8)
        vLayout.addWidget(self.longrange)
        vLayout.addStretch()
        vLayout.addLayout(FormLay([[self.prob_label,self.probrewire],
                                         [self.freq_label,self.freqrewire]]))
        grpBox = QtWidgets.QGroupBox("Neighbourhood  ")
        grpBox.setLayout(vLayout)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(grpBox)
        self.setLayout(layout)


class Animate(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tstart = SpinBox(10000,10)
        self.tend = SpinBox(100000,10)
        self.delay_spBox = DoubleSpinBox(0.05, 5.0, 0.5)
        self.animate_but = QtWidgets.QPushButton("Animate!")
        self.pltSr_but = QtWidgets.QPushButton("Plot Time Series")
        self.set_all_layouts()

    def get_values(self):
        return (int(self.tstart.value()),
                int(self.tend.value()),
                self.delay_spBox.value() )

    def set_all_layouts(self):
        self.tstart.setValue(0)
        self.tend.setValue(50)
        self.delay_spBox.setValue(0.2)
        st1_label = QtWidgets.QLabel("Start time")
        et2_label = QtWidgets.QLabel("End time")
        delay_label = QtWidgets.QLabel("Delay(secs)")
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(FormLay([[st1_label,   self.tstart],
                                   [et2_label,   self.tend],
                                   [delay_label, self.delay_spBox]]) )
        vLayout.addStretch()
        vLayout.addWidget(self.animate_but)
        vLayout.addWidget(self.pltSr_but)
        grpBox = QtWidgets.QGroupBox("Animate")
        grpBox.setLayout(vLayout)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(grpBox)
        self.setLayout(layout)


class Controls(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initpop = Initpop()
        self.nbrhd = Neighbourhood()
        self.anim = Animate()
        self.set_all_layouts()
        self.initpop.newValueSelected.connect(self.disable_plot_buttons)

    def disable_plot_buttons(self, disable=True):
        self.anim.animate_but.setDisabled(disable)
        self.anim.pltSr_but.setDisabled(disable)
        self.initpop.plot_but.setDisabled(disable)

    def set_all_layouts(self):
        self.setWindowTitle("S I R Model")
        centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralwidget)
        horizontalLayout = QtWidgets.QHBoxLayout(centralwidget)
        horizontalLayout.addWidget(self.initpop)
        horizontalLayout.addWidget(self.nbrhd)
        horizontalLayout.addWidget(self.anim)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')



if __name__ == '__main__':
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    form = Initpop()
    form.show()
    # sys.exit(app.exec_())
