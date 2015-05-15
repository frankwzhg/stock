#! /usr/bin/python
# -*-coding: utf-8 -*-

import sys
from pandas.lib import duplicated
from top_stocksUI import *
from matplotlib.font_manager import FontProperties
from matplotlibwidget import *
from rate_plot import *
import pandas as pd
import dateutil
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

class GUIForm(QtGui.QMainWindow):

# inital mainwindows

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
        # self.fund_rate = self.fund_rate()
        # self.fund_data = self.fund_data()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.fund_cat.addItems([u"封闭式基金", u"ETF基金", u"LOF基金", u"创新性基金"])
        self.ui.fund_code.addItems(self.get_fund_code())
        self.ui.F_rate.setText(self.fund_rate())
        self.top_stock_table()
        self.draw_today_Pnet()
        # self.eventFilter(self.ui.widget.canvas.period_percent_rate)
        self.my_con()
        #
        # print self.get_fund_code()
        #
        # print self.fund_rate()

# get fund code under condition selected
    def get_fund_code(self):

        fund_data = self.fund_data()
        fund_code = list(fund_data.code.drop_duplicates('code'))
        return fund_code

#get table name follow combobox change

    def table_name(self):

        if(self.ui.fund_cat.currentIndex() == 0):
            table_name_rate = "test.fund_Close_rate"
            table_name_cal = "test.fund_Close_cal"
        elif(self.ui.fund_cat.currentIndex() == 1):
            table_name_rate = "test.fund_ETF_rate"
            table_name_cal = "test.fund_ETF_cal"
        elif(self.ui.fund_cat.currentIndex() == 2):
            table_name_rate = "test.fund_LOF_rate"
            table_name_cal = "test.fund_LOF_cal"
        else:
            table_name_rate = "test.fund_creative_rate"
            table_name_cal = "test.fund_creative_cal"

        return (table_name_rate, table_name_cal)



# get fund rate under fund selected

    def fund_rate(self):
        fund_code = self.ui.fund_code.currentText()
        self.fund_date = self.ui.fund_date.date().toPyDate()
        table_name = self.table_name()[0]
        sql_script = "select rate from %s where get_date = '%s' and code = '%s'" % (table_name, str(self.fund_date), fund_code)
        fund_rate = read(sql_script)
        # print fund_rate.ix[0, 0]
        # fund_rate = str(float("{0:.3f}".format(fund_rate.ix[0, 0])))
        fund_rate = '%.3f' % fund_rate.ix[0, 0]
        return fund_rate

# get all data from fund cal table in database
    def fund_data(self):
        table_name = self.table_name()[1]
        fund_date = self.ui.fund_date.date().toPyDate()
        sql_script = "select * from %s where get_date = '%s'" % (table_name, fund_date)
        fund_data_all = read(sql_script)

        return fund_data_all
    # define event to change value

    def my_con(self):

        QtCore.QObject.connect(self.ui.fund_cat, QtCore.SIGNAL('activated(QString)'), self.update_fund_cat)
        QtCore.QObject.connect(self.ui.fund_cat, QtCore.SIGNAL('activated(QString)'), self.top_stock_table)
        QtCore.QObject.connect(self.ui.fund_cat, QtCore.SIGNAL('activated(QString)'), self.draw_today_Pnet)
        QtCore.QObject.connect(self.ui.fund_code, QtCore.SIGNAL('activated(QString)'), self.update_fund_code)
        QtCore.QObject.connect(self.ui.fund_code, QtCore.SIGNAL('activated(QString)'), self.top_stock_table)
        QtCore.QObject.connect(self.ui.fund_code, QtCore.SIGNAL('activated(QString)'), self.draw_today_Pnet)
        QtCore.QObject.connect(self.ui.fund_date, QtCore.SIGNAL('dateChanged(QDate)'), self.update_fund_date)
        QtCore.QObject.connect(self.ui.fund_date, QtCore.SIGNAL('dateChanged(QDate)'), self.top_stock_table)
        QtCore.QObject.connect(self.ui.fund_date, QtCore.SIGNAL('dateChanged(QDate)'), self.draw_today_Pnet)
        self.ui.widget.canvas.mpl_connect('motion_notify_event', self.move_on)
        # self.ui.widget.canvas.setMouseTracking(True)
        # self.ui.widget.canvas.installEventFilter(self)

        # self.ui.widget.canvas.mpl_connect('pick_event', self.on_pick)
        # self.ui.widget.canvas.mpl_connect('pick_event', self.on_pick)
        # self.ui.widget.canvas.mpl_connect('button_release_event', self.offclick)

    # update window data value when fund_cat changed

    def update_fund_cat(self):

        self.ui.fund_code.clear()
        self.ui.fund_code.addItems(self.get_fund_code())
        self.ui.F_rate.setText(self.fund_rate())
    #update window data value when fund_code change

    def update_fund_code(self):

        self.ui.F_rate.setText(self.fund_rate())

    # update window data value when fund date change
    def update_fund_date(self):
        self.update_fund_cat()

    #get top_stocks for each fund
    def get_top_stocks(self):
        table_name = self.table_name()[1]
        get_date = self.ui.fund_date.date().toPyDate()
        fund_code = self.ui.fund_code.currentText()
        sql_script = "select stock_code, percent_net, percent_net_now from %s where get_date = '%s' and code = '%s'" % (table_name, get_date, fund_code)
        top_stocks = read(sql_script)
        # top_stocks = self.fund_data()[self.fund_data().code == fund_code]
        # print top_stocks
        # top_stocks = top_stocks[["stock_code", "percent_net", "percent_net_now"]]
        top_stocks["percent_net"] = top_stocks["percent_net"].map(lambda x: '%.3f' %x)
        top_stocks["percent_net_now"] = top_stocks["percent_net_now"].map(lambda x: '%.3f' %x)
        return top_stocks

    # setup top stock table on gui
    def top_stock_table(self):
        top_stocks_data = self.get_top_stocks()
        self.ui.top_stocks.setColumnCount(len(top_stocks_data.columns))
        self.ui.top_stocks.setRowCount(len(top_stocks_data.index))
        self.ui.top_stocks.setHorizontalHeaderLabels([u"代码", u"官方比率", u"计算比率"])
        for i in range(len(top_stocks_data.index)):
            for j in range(len(top_stocks_data.columns)):
                self.ui.top_stocks.setItem(i, j, QtGui.QTableWidgetItem(str(top_stocks_data.iget_value(i, j))))

    def draw_today_Pnet(self):
        input_day = self.ui.fund_date.date()
        start_day = QtCore.QDate.addDays(input_day, -3).toPyDate()
        end_day = input_day.toPyDate()
        # print end_day, start_day
        table_name = self.table_name()
        fund_code = self.ui.fund_code.currentText()

        draw_data_sql = "select code, stock_code, percent_net, percent_net_now, get_date from %s where code = '%s' and get_date>= '%s' and get_date < '%s'" % (table_name[1], fund_code, start_day, end_day)
        draw_data = read(draw_data_sql)
        # print draw_data
        x = draw_data.get_date.drop_duplicates('get_date')
        # print list(x)
        bar_width = 0.35

        self.ui.widget.canvas.period_percent_rate.clear()
        self.ui.widget.canvas.period_percent_rate.set_title(u'十大股票基金中比率变化图', fontproperties = self.ChineseFont1)
        self.ui.widget.canvas.period_percent_rate.xaxis.set_major_locator(MultipleLocator(10))
        self.points_with_annotation = []
        for i in draw_data.index:
            # point_com, = self.ui.widget.canvas.period_percent_rate.plot(draw_data.index, draw_data.percent_net, 'ro', markersize=10)
            bar_com = self.ui.widget.canvas.period_percent_rate.bar(draw_data.index, draw_data.percent_net, bar_width, color = 'b', picker = 5)
            print bar_com
            annotation = self.ui.widget.canvas.period_percent_rate.annotate("this is a test", xy=(draw_data.index[i], draw_data.percent_net[i]), xytext=(draw_data.index[i]+0.5, draw_data.percent_net[i]))
            annotation.set_visible(False)
            self.points_with_annotation.append([bar_com, annotation])
        bar_cal = self.ui.widget.canvas.period_percent_rate.bar(draw_data.index+bar_width, draw_data.percent_net_now, bar_width, color = 'y', picker = 5)
        # bar_com = self.ui.widget.canvas.period_percent_rate.plot(draw_data.percent_net, color = 'b')

        # bar_cal = self.ui.widget.canvas.period_percent_rate.plot(draw_data.percent_net_now, color = 'y')
        # pione_cal, = self.ui.widget.canvas.period_percent_rate.plot(draw_data.index, draw_data.percent_net_now, 'go')
        self.ui.widget.canvas.period_percent_rate.legend([bar_com, bar_cal], [u'公司公布', u'重新计算'])
        self.ui.widget.canvas.period_percent_rate.xaxis.grid(True, which='major')
        self.ui.widget.canvas.period_percent_rate.yaxis.grid(True)
        self.ui.widget.canvas.period_percent_rate.set_ylim(0, max(draw_data.percent_net_now)+max(draw_data.percent_net_now) * 0.2)
        self.ui.widget.canvas.period_percent_rate.set_xticklabels(['0'] + ['0'] + list(x))



        # print self.points_with_annotation
        # print draw_data
        # self.ui.widget.canvas.draw()
        return self.points_with_annotation

    # define mouse clicks events
    def on_pick(self, event):
        # ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
        artist = event.artist
        print artist
        x = artist.get_bbox().x0
        y = artist.get_bbox().y1
        my_data = self.draw_today_Pnet()
        stock_code = my_data[my_data.index == int(x)]['stock_code']
        stock_code = stock_code.ix[int(x), 0]
        self.text = self.ui.widget.canvas.period_percent_rate.text(x, y, u'股票代码: %s' % stock_code, fontproperties = self.ChineseFont1)
        # self.text.set_text("")
        self.ui.widget.canvas.draw()
        print x
        print y
        return (x, y)

    def offclick(self, event):
        try:
            self.text.remove()
            self.ui.widget.canvas.draw()
        except:
            pass

    def eventFilter(self, obj, event):
        if(obj == self.ui.widget):
            print "test"
        if (event.type() == QtCore.QEvent.MouseButtonPress):
            self.ui.widget.canvas.mpl_connect('pick_event', self.on_pick)
        if (event.type() == QtCore.QEvent.MouseButtonDblClick):
            print "obj"

    def move_on(self, event):

        visibility_changed = False
        for bar, annotation in self.draw_today_Pnet():
            should_be_visible = (bar.contains(event)[0] == True)
            print bar.contains()

            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)

        if visibility_changed:
            self.ui.widget.canvas.draw()




def main():
    app = QtGui.QApplication(sys.argv)
    gui = GUIForm()
    gui.show()
    app.exec_()

if __name__ == "__main__":

    main()