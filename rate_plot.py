#! /usr/bin/python
#  -*- coding: utf-8 -*-

import sys
from rate_plotUI import *
from op_database import *
from matplotlib.font_manager import FontProperties
from matplotlibwidget import *
import dateutil

class GUIForm(QtGui.QDialog):

    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)


        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.RatePlotUpdate()
        QtCore.QObject.connect(self.ui.fund_cat, QtCore.SIGNAL('activated(QString)'), self.RatePlotUpdate)
        QtCore.QObject.connect(self.ui.R_date_input, QtCore.SIGNAL('dateChanged(QDate)'), self.RatePlotUpdate)
        QtCore.QObject.connect(self.ui.max_rate, QtCore.SIGNAL('valueChanged(double)'), self.RatePlotUpdate)
        QtCore.QObject.connect(self.ui.min_rate, QtCore.SIGNAL('valueChanged(double)'), self.RatePlotUpdate)
        self.ui.widget.canvas.mpl_connect('pick_event', self.on_pick)


    def plot_data(self):
        # print self.ui.fund_cat.currentIndex()
        if(self.ui.fund_cat.currentIndex() == 0):
            table_name = "test.fund_creative_rate"
        elif(self.ui.fund_cat.currentIndex() == 1):
            table_name = "test.fund_ETF_rate"
        elif(self.ui.fund_cat.currentIndex() == 2):
            table_name = "test.fund_LOF_rate"
        else:
            table_name = "test.fund_Close_rate"
        sel_date = self.ui.R_date_input.date().toPyDate()
        max_rate = self.ui.max_rate.value()
        min_rate = self.ui.min_rate.value()
        rate_data = read("select * from " + table_name + " where get_date = '" + str(sel_date) + "'")
        plot_data = rate_data[(rate_data.rate >= min_rate) & (rate_data.rate <= max_rate)]
        return (plot_data, table_name)

    def RatePlotUpdate(self):
        # posit = self.ui.max_rate.value()-5
        ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
        plot_data, table_name = self.plot_data()
        # print table_name
        self.ui.widget.canvas.rate.clear()
        self.ui.widget.canvas.rate.set_title(u"当天折溢率分布图", fontproperties = ChineseFont1)

        if len(plot_data) > 0:
            self.ui.widget.canvas.rate.scatter(plot_data.index, plot_data.rate, picker = 5)
            self.ui.widget.canvas.rate.set_xlim(-5, max(plot_data.index)+5)
            self.text = self.ui.widget.canvas.rate.text(0, max(plot_data.rate), u'请选择一个点', fontproperties = ChineseFont1)
        else:
            self.ui.widget.canvas.rate.text(0.25, 1.5, "this is empty dataframe")
        self.ui.widget.canvas.draw()
        return plot_data

    def on_pick(self, event):

        ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
        ind = event.ind[0]
        # print ind
        fund_data, table_name = self.plot_data()
        fund_data = fund_data.reindex(index = range(len(fund_data)))
        # print fund_data
        code_data = fund_data[fund_data.index == ind]
        fund_code = code_data.ix[ind, 0]
        print fund_code
        if(len(code_data) > 0):

            draw_data = read("select * from " + table_name + " where code = '" + fund_code + "'")
            # print len(draw_data)
            draw_data['get_date'] = [dateutil.parser.parse(x) for x in draw_data['get_date']]
            max_rate = self.ui.max_rate.value()
            min_rate = self.ui.min_rate.value()
            draw_data = draw_data[(draw_data.rate >= min_rate) & (draw_data.rate <= max_rate)]
            # print draw_data.rate
            self.ui.widget.canvas.fund.clear()
            self.ui.widget.canvas.fund.set_title(u'选择基金折溢率变化曲线', fontproperties = ChineseFont1)
            self.ui.widget.canvas.fund.plot(draw_data.get_date, draw_data.rate)
            self.text.set_text(u'您选择的基金代码: %s'%str(fund_code))
        else:
            self.ui.widget.canvas.fund.clear()
            self.ui.widget.canvas.fund.plot()
            # self.ui.widget.canvas.fund.text(0, 0, "testtest")
            self.text.set_text(u"您选择的基金没有历史数据")
        self.ui.widget.canvas.draw()
        # return fund_code


def main():
    app = QtGui.QApplication(sys.argv)
    gui = GUIForm()
    gui.show()
    app.exec_()
if __name__ == "__main__":
    main()



