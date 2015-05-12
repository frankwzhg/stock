# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rate_plotUI.ui'
#
# Created: Wed May  6 09:25:21 2015
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
        # Dialog.resize(745, 521)
        Dialog.resize(900, 600)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.R_date_label = QtGui.QLabel(Dialog)
        self.R_date_label.setObjectName(_fromUtf8("R_date_label"))
        self.horizontalLayout.addWidget(self.R_date_label)
        self.R_date_input = QtGui.QDateEdit(Dialog)
        # self.R_date_input.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        # self.R_date_input = QtGui.QDateEdit(self.layoutWidget)
        self.R_date_input.setDate(QtCore.QDate.addDays(QtCore.QDate.currentDate(), -1))
        # self.R_date_input.setDate(QtCore.QDate(2000, 1, 1))
        self.R_date_input.setCalendarPopup(True)
        self.R_date_input.setObjectName(_fromUtf8("R_date_input"))
        self.horizontalLayout.addWidget(self.R_date_input)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.max_rate = QtGui.QDoubleSpinBox(Dialog)
        self.max_rate.setProperty("value", 50.0)
        self.max_rate.setObjectName(_fromUtf8("max_rate"))
        self.horizontalLayout.addWidget(self.max_rate)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.min_rate = QtGui.QDoubleSpinBox(Dialog)
        self.min_rate.setMinimum(-100.0)
        self.min_rate.setProperty("value", -50.0)
        self.min_rate.setObjectName(_fromUtf8("min_rate"))
        self.horizontalLayout.addWidget(self.min_rate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.R_date_plot = QtGui.QLabel(Dialog)
        self.R_date_plot.setObjectName(_fromUtf8("R_date_plot"))
        self.gridLayout.addWidget(self.R_date_plot, 0, 0, 1, 1)
        self.widget = matplotlibWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 1, 2, 1)
        self.R_date_fund_plot = QtGui.QLabel(Dialog)
        self.R_date_fund_plot.setWordWrap(True)
        self.R_date_fund_plot.setObjectName(_fromUtf8("R_date_fund_plot"))
        self.gridLayout.addWidget(self.R_date_fund_plot, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        # QtCore.QObject.connect(self.R_date_input, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), self.R_date_plot.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.R_date_label.setText(_translate("Dialog", "折溢率日期：", None))
        self.label.setText(_translate("Dialog", "最大折溢率(%):", None))
        self.label_2.setText(_translate("Dialog", "最小折溢率(%):", None))
        self.R_date_plot.setText(_translate("Dialog", "当日折溢率：", None))
        self.R_date_fund_plot.setText(_translate("Dialog", "选择基金折溢率变化：", None))

from matplotlibwidget import matplotlibWidget
