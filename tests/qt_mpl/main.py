# baseado em: 
#    https://www.boxcontrol.net/embedding-matplotlib-plot-on-pyqt5-gui.html
#    http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies

# facilita uso de todos objetos Qt (ex: qt.QPushButton, qt.Qt.Key_Escape)
from PyQt4 import Qt as qt

import matplotlib
matplotlib.use("Qt4Agg")

from matplotlib.figure import Figure as MplFigure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg

from numpy import arange, sin, pi


class MyMplCanvas(FigureCanvasQTAgg):
    '''
    A classe FigureCanvasQTAgg herda QWidget.
    '''
    def __init__(self):
        # contém primitivas de matplotlib
        self.fig = MplFigure()
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)

        # inicializa FigureCanvasQTAgg com um objeto Figure
        super().__init__(self.fig)
        # self.plot()

    def plot(self, R1, R2, RXmin, RXmax, V0):
        # print(self.parent().parent().)
        # print('baka', self.parent().parent().r1_edit.text())

        def f(RX, R1, R2, V0):
            return V0*(R1/(R1+R2) - RX/(R1+RX))
        RX = arange(RXmin, RXmax, (RXmax - RXmin)/200)
        V = f(RX, R1, R2, V0)
        self.axes.plot(RX, V)
        self.draw()


class MyWindow(qt.QMainWindow):
    '''
    Janela principal.
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Plot Area
        self.mpl_canvas = MyMplCanvas()
        self.mpl_toolbar = NavigationToolbar2QTAgg(self.mpl_canvas, self)

        mpl_layout = qt.QVBoxLayout()
        mpl_layout.addWidget(self.mpl_canvas)
        mpl_layout.addWidget(self.mpl_toolbar)


        mpl_area = qt.QWidget()
        mpl_area.setLayout(mpl_layout)
        self.setCentralWidget(mpl_area)
        self.config_dock = self.initDockArea()
        self.addDockWidget(qt.Qt.LeftDockWidgetArea, self.config_dock)


    def initDockArea(self):
        # Config Area
        config_dock = qt.QDockWidget()
        config_dock.setFixedWidth(200)

        config_toolbar_grid = qt.QGridLayout()
        config_toolbar_grid.setSpacing(10)

        equation_label = qt.QSvgWidget('CodeCogsEqn.svg')

        r1_label = qt.QLabel('R1:')
        self.r1_edit = qt.QLineEdit()
        self.r1_edit.textChanged[str].connect(self.generateBttClicked)

        r2_label = qt.QLabel('R2:')
        self.r2_edit = qt.QLineEdit()

        rx_label = qt.QLabel('RX:')

        min_label = qt.QLabel('Min')
        self.min_edit = qt.QLineEdit()
        max_label = qt.QLabel('Max')
        self.max_edit = qt.QLineEdit()

        volt_label = qt.QLabel('V:')
        self.volt_edit = qt.QLineEdit()

        generate_btt = qt.QPushButton('Generate')
        generate_btt.clicked.connect(self.generateBttClicked)

        config_toolbar_grid.addWidget(equation_label, 0, 0, 1, 2)
        config_toolbar_grid.addWidget(r1_label, 1, 0)
        config_toolbar_grid.addWidget(self.r1_edit, 1, 1)
        config_toolbar_grid.addWidget(r2_label, 2, 0)
        config_toolbar_grid.addWidget(self.r2_edit, 2, 1)
        config_toolbar_grid.addWidget(rx_label, 3, 0, 1, 2)
        config_toolbar_grid.addWidget(min_label, 4, 0)
        config_toolbar_grid.addWidget(self.min_edit, 4, 1)
        config_toolbar_grid.addWidget(max_label, 5, 0)
        config_toolbar_grid.addWidget(self.max_edit, 5, 1)
        config_toolbar_grid.addWidget(volt_label, 6, 0)
        config_toolbar_grid.addWidget(self.volt_edit, 6, 1)

        config_layout = qt.QVBoxLayout()
        config_layout.addLayout(config_toolbar_grid)
        config_layout.addStretch()
        config_layout.addWidget(generate_btt)

        config_widget = qt.QWidget()
        config_widget.setLayout(config_layout)
        config_dock.setWidget(config_widget)

        return config_dock

    def generateBttClicked(self):
        #try:
            self.mpl_canvas.plot(
                float(self.r1_edit.text()),
                float(self.r2_edit.text()),
                float(self.min_edit.text()),
                float(self.max_edit.text()),
                float(self.volt_edit.text())
                )
        # except:
        #     pass

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == qt.Qt.Key_Escape:
            self.close()


def main():
    app = qt.QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
