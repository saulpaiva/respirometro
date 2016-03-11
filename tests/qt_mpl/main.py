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
        self.mpl_canvas = MyMplCanvas()
        self.mpl_toolbar = NavigationToolbar2QTAgg(self.mpl_canvas, self)

        layout = qt.QVBoxLayout()
        layout.addWidget(self.mpl_canvas)
        layout.addWidget(self.mpl_toolbar)
        self.setLayout(layout)

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
