# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'top_stocksUI.ui'
#
# Created: Fri May 15 10:17:08 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(854, 548)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.fund_cat = QtGui.QComboBox(self.centralwidget)
        self.fund_cat.setObjectName(_fromUtf8("fund_cat"))
        self.gridLayout.addWidget(self.fund_cat, 1, 1, 1, 2)
        self.top_stocks = QtGui.QTableWidget(self.centralwidget)
        self.top_stocks.setRowCount(10)
        self.top_stocks.setColumnCount(3)
        self.top_stocks.setObjectName(_fromUtf8("top_stocks"))
        self.top_stocks.horizontalHeader().setCascadingSectionResizes(False)
        self.top_stocks.horizontalHeader().setStretchLastSection(False)
        self.top_stocks.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.top_stocks, 1, 3, 4, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.fund_code = QtGui.QComboBox(self.centralwidget)
        self.fund_code.setEditable(True)
        self.fund_code.setObjectName(_fromUtf8("fund_code"))
        self.gridLayout.addWidget(self.fund_code, 2, 1, 1, 2)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.fund_date = QtGui.QDateEdit(self.centralwidget)
        self.fund_date.setDate(QtCore.QDate.addDays(QtCore.QDate.currentDate(), -1))
        self.fund_date.setCalendarPopup(True)
        self.fund_date.setObjectName(_fromUtf8("fund_date"))
        self.gridLayout.addWidget(self.fund_date, 3, 1, 1, 2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 2)
        self.F_rate = QtGui.QLabel(self.centralwidget)
        self.F_rate.setObjectName(_fromUtf8("F_rate"))
        self.gridLayout.addWidget(self.F_rate, 4, 2, 1, 1)
        self.widget = top_stock_mat(self.centralwidget)
        self.widget.setEnabled(True)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 5, 0, 1, 4)
        self.gridLayout.setRowStretch(5, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 854, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_5.setText(_translate("MainWindow", "基金前十重仓股票", None))
        self.label.setText(_translate("MainWindow", "基金类别:", None))
        self.label_2.setText(_translate("MainWindow", "基金代码:", None))
        self.label_4.setText(_translate("MainWindow", "数据日期:", None))
        self.label_3.setText(_translate("MainWindow", "基金当前净值:", None))
        self.F_rate.setText(_translate("MainWindow", "0.00", None))

from top_stock_mat import top_stock_mat
