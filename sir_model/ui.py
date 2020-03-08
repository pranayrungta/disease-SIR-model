from PyQt5 import QtWidgets

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

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.singleinfected = QtWidgets.QCheckBox("Single Infected Individual")
        s0_label = QtWidgets.QLabel("So:")
        i0_label = QtWidgets.QLabel("Io:")
        r0_label = QtWidgets.QLabel("Ro:")
        size_label = QtWidgets.QLabel("Size:")
        self.s0 = DoubleSpinBox()
        self.i0 = DoubleSpinBox()
        self.r0 = DoubleSpinBox()
        self.popsize = SpinBox(200, 10)
        self.generatebutton = QtWidgets.QPushButton("Generate")
        self.plot_but = QtWidgets.QPushButton("Plot")

        initPopPara_Layout = QtWidgets.QVBoxLayout()
        initPopPara_Layout.addWidget(self.singleinfected)
        initPopPara_Layout.addLayout(FormLay([[s0_label,   self.s0],
                                              [i0_label,   self.i0],
                                              [r0_label,   self.r0],
                                              [size_label, self.popsize]]))
        initPopPara_Layout.addStretch()
        initPopPara_Layout.addWidget(self.generatebutton)
        initPopPara_Layout.addWidget(self.plot_but)
        InitPop_grpBox = QtWidgets.QGroupBox("Initial Population")
        InitPop_grpBox.setLayout(initPopPara_Layout)
        #==============================================================

        self.nbr4 = QtWidgets.QRadioButton("von Neumann(4)")
        self.nbr4.setChecked(True)
        self.nbr8 = QtWidgets.QRadioButton("Moore(8)")
        self.longrange = QtWidgets.QCheckBox("Long Range Interactions")
        self.prob_label = QtWidgets.QLabel("Probability:")
        self.probrewire = QtWidgets.QLineEdit()
        self.freq_label = QtWidgets.QLabel("Frequency:")
        self.freqrewire = QtWidgets.QLineEdit()

        nbrHd_vLayout = QtWidgets.QVBoxLayout()
        nbrHd_vLayout.addWidget(self.nbr4)
        nbrHd_vLayout.addWidget(self.nbr8)
        nbrHd_vLayout.addWidget(self.longrange)
        nbrHd_vLayout.addStretch()
        nbrHd_vLayout.addLayout(FormLay([[self.prob_label,self.probrewire],
                                         [self.freq_label,self.freqrewire]]))
        NbrHd_grpBox = QtWidgets.QGroupBox("Neighbourhood  ")
        NbrHd_grpBox.setLayout(nbrHd_vLayout)
        #=================================================================

        st1_label = QtWidgets.QLabel("Start time")
        self.tstart = SpinBox(10000,10)
        et2_label = QtWidgets.QLabel("End time")
        self.tend = SpinBox(100000,10)
        delay_label = QtWidgets.QLabel("Delay(secs)")
        self.delay_spBox = DoubleSpinBox(0.05, 5.0, 0.5)
        self.delay_spBox.setValue(0.2)
        time_layout = FormLay([[st1_label,   self.tstart],
                               [et2_label,   self.tend],
                               [delay_label, self.delay_spBox]])
        self.animate_but = QtWidgets.QPushButton("Animate!")
        self.pltSr_but = QtWidgets.QPushButton("Plot Time Series")

        Animate_vLayout = QtWidgets.QVBoxLayout()
        Animate_vLayout.addLayout(time_layout)
        Animate_vLayout.addStretch()
        Animate_vLayout.addWidget(self.animate_but)
        Animate_vLayout.addWidget(self.pltSr_but)
        Anim_grpBox = QtWidgets.QGroupBox("Animate")
        Anim_grpBox.setLayout(Animate_vLayout)
        #================================================================

        self.setWindowTitle("S I R Model")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        horizontalLayout.addWidget(InitPop_grpBox)
        horizontalLayout.addWidget(NbrHd_grpBox)
        horizontalLayout.addWidget(Anim_grpBox)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Working...')


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = UI()
    form.show()
    sys.exit(app.exec_())
