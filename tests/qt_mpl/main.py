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
        self.plot()

    def plot(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyWindow(qt.QWidget):
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

        # Config Area
        config_area = qt.QWidget()
        config_area.setFixedWidth(200)

        config_toolbar_grid = qt.QGridLayout()
        config_toolbar_grid.setSpacing(10)

        equation_label = qt.QLabel('V*[R1/(R1+R2) - RX/(R1+RX)]')

        r1_label = qt.QLabel('R1:')
        r1_edit = qt.QLineEdit()

        r2_label = qt.QLabel('R2:')
        r2_edit = qt.QLineEdit()

        rx_label = qt.QLabel('RX:')
        rx_edit = qt.QLineEdit()

        min_label = qt.QLabel('Min')
        min_edit = qt.QLineEdit()
        max_label = qt.QLabel('Max')
        max_edit = qt.QLineEdit()

        volt_label = qt.QLabel('V:')
        volt_edit = qt.QLineEdit()

        generate_btt = qt.QPushButton('Generate')

        config_toolbar_grid.addWidget(equation_label, 0, 0, 1, 2)
        config_toolbar_grid.addWidget(r1_label, 1, 0)
        config_toolbar_grid.addWidget(r1_edit, 1, 1)
        config_toolbar_grid.addWidget(r2_label, 2, 0)
        config_toolbar_grid.addWidget(r2_edit, 2, 1)
        config_toolbar_grid.addWidget(rx_label, 3, 0, 1, 2)
        config_toolbar_grid.addWidget(min_label, 4, 0)
        config_toolbar_grid.addWidget(min_edit, 4, 1)
        config_toolbar_grid.addWidget(max_label, 5, 0)
        config_toolbar_grid.addWidget(max_edit, 5, 1)
        config_toolbar_grid.addWidget(volt_label, 6, 0)
        config_toolbar_grid.addWidget(volt_edit, 6, 1)
        
        config_layout = qt.QVBoxLayout()
        config_layout.addLayout(config_toolbar_grid)
        config_layout.addStretch()
        config_layout.addWidget(generate_btt)

        # Main Area
        main_layout = qt.QGridLayout()
        main_layout.addLayout(mpl_layout, 0, 0, 1, 2)
        main_layout.addLayout(config_layout, 0, 2, 1, 1)
        self.setLayout(main_layout)
        
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
