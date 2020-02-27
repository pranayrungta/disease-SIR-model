from PyQt5 import QtWidgets

def DoubleSpinBox(maximum, singleStep):
    box = QtWidgets.QDoubleSpinBox()
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
    return box

def SpinBox(maximum, singleStep):
    box = QtWidgets.QSpinBox()
    box.setMaximum(maximum)
    box.setSingleStep(singleStep)
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
        self.s0_label = QtWidgets.QLabel("So:")
        self.s0 = DoubleSpinBox(1.0, 0.1)
        self.i0_label = QtWidgets.QLabel("Io:")
        self.i0 = DoubleSpinBox(1.0, 0.1)
        self.r0_label = QtWidgets.QLabel("Ro:")
        self.r0 = DoubleSpinBox(1.0, 0.1)        
        self.size_label = QtWidgets.QLabel("Size:")
        self.popsize = SpinBox(200, 10)
        self.popsize.setProperty("value", 0)
        self.generatebutton = QtWidgets.QPushButton("Generate")
        self.plot_but = QtWidgets.QPushButton("Plot")
        
        initPopPara_Layout = QtWidgets.QVBoxLayout()
        initPopPara_Layout.addWidget(self.singleinfected)
        initPopPara_Layout.addLayout(FormLay([[self.s0_label,  self.s0], 
                                              [self.i0_label,  self.i0], 
                                              [self.r0_label,  self.r0], 
                                              [self.size_label,self.popsize]]))
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
        
        self.st1_label = QtWidgets.QLabel("Start at t1")
        self.tstart = SpinBox(10000,10)
        self.tstart.setProperty("value", 0)
        self.et2_label = QtWidgets.QLabel("End at t2")
        self.tend = SpinBox(100000,10)
        self.tend.setProperty("value", 0)
        self.dely_label = QtWidgets.QLabel("Delay(secs)")
        self.delay_spBox = DoubleSpinBox(5.0, 0.5)
        self.delay_spBox.setMinimum(0.05)
        self.delay_spBox.setValue(0.2)
        self.animate_but = QtWidgets.QPushButton("Animate!")
        self.pltSr_but = QtWidgets.QPushButton("Plot Time Series")


        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(self.st1_label,   0, 0, 1, 1)
        gridLayout.addWidget(self.tstart,      1, 0, 1, 1)
        gridLayout.addWidget(self.et2_label,   0, 1, 1, 1)
        gridLayout.addWidget(self.tend,        1, 1, 1, 1)
        gridLayout.addWidget(self.dely_label,  2, 0, 1, 1)
        gridLayout.addWidget(self.delay_spBox, 2, 1, 1, 1)
        anim_Plot_HLayout = QtWidgets.QHBoxLayout()
        anim_Plot_HLayout.addWidget(self.animate_but)
        anim_Plot_HLayout.addWidget(self.pltSr_but)
        Animate_vLayout = QtWidgets.QVBoxLayout()
        Animate_vLayout.addLayout(gridLayout)
        Animate_vLayout.addLayout(anim_Plot_HLayout)
        Animate_vLayout.addStretch()
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
