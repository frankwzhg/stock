import sys
from PyQt4 import QtCore, QtGui, uic


class test(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('test.ui', self)

        self.connect(self.ui.graphicsView, QtCore.SIGNAL("mousePressEvent()"), self.mouse_pressed)
        self.connect(self.ui.graphicsView, QtCore.SIGNAL("mouseMoveEvent()"), self.mouse_moved)
        self.connect(self.ui.graphicsView, QtCore.SIGNAL("mouseReleaseEvent()"), self.mouse_released)

        self.ui.show()

    def mouse_pressed(self):
        p = QtGui.QCursor.pos()
        print "pressed here: " + p.x() + ", " + p.y()

    def mouse_moved(self):
        p = QtGui.QCursor.pos()
        print "moved here: " + p.x() + ", " + p.y()

    def mouse_released(self):
        p = QtGui.QCursor.pos()
        print "released here: " + p.x() + ", " + p.y()


def main():
    app = QtGui.QApplication(sys.argv)
    ui = test()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()