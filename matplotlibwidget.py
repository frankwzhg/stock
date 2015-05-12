#!/usr/bin/python
# -*-coding: utf-8 -*-

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.rate = self.fig.add_subplot(211)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.canvas.mpl_connect('pick_event', self.onclick)

        # self.dpi = 100
        # self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.main_frame)

        self.fund = self.fig.add_subplot(212)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def onclick(self):
        print 'tst'

class matplotlibWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

