# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rate_plotUI.ui'
#
# Created: Mon May  4 11:03:18 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(666, 470)
        self.R_date_plot = QtGui.QLabel(Dialog)
        self.R_date_plot.setGeometry(QtCore.QRect(30, 140, 81, 21))
        self.R_date_plot.setObjectName(_fromUtf8("R_date_plot"))
        self.R_date_fund_plot = QtGui.QLabel(Dialog)
        self.R_date_fund_plot.setGeometry(QtCore.QRect(30, 300, 81, 51))
        self.R_date_fund_plot.setWordWrap(True)
        self.R_date_fund_plot.setObjectName(_fromUtf8("R_date_fund_plot"))
        self.widget = matplotlibWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(159, 79, 491, 381))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 601, 29))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.R_date_label = QtGui.QLabel(self.layoutWidget)
        self.R_date_label.setObjectName(_fromUtf8("R_date_label"))
        self.gridLayout.addWidget(self.R_date_label, 0, 0, 1, 1)
        self.R_date_input = QtGui.QDateEdit(self.layoutWidget)
        self.R_date_input.setDate(QtCore.QDate.addDays(QtCore.QDate.currentDate(), -1))
        self.R_date_input.setCalendarPopup(True)
        self.R_date_input.setObjectName(_fromUtf8("R_date_input"))
        self.gridLayout.addWidget(self.R_date_input, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.max_rate = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.max_rate.setProperty("value", 50.0)
        self.max_rate.setObjectName(_fromUtf8("max_rate"))
        self.gridLayout.addWidget(self.max_rate, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.min_rate = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.min_rate.setMinimum(-100.0)
        self.min_rate.setProperty("value", -50.0)
        self.min_rate.setObjectName(_fromUtf8("min_rate"))
        self.gridLayout.addWidget(self.min_rate, 0, 5, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.R_date_input, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.R_date_plot.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.R_date_plot.setText(_translate("Dialog", "当日折溢率：", None))
        self.R_date_fund_plot.setText(_translate("Dialog", "选择基金折溢率变化：", None))
        self.R_date_label.setText(_translate("Dialog", "折溢率日期：", None))
        self.label.setText(_translate("Dialog", "最大折溢率(%):", None))
        self.label_2.setText(_translate("Dialog", "最小折溢率(%):", None))

from matplotlibwidget import matplotlibWidget
