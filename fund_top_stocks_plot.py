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
from datetime import timedelta
import matplotlib.pyplot as plt

class GUIForm(QtGui.QMainWindow):

# inital mainwindows

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        # self.ChineseFont1 = FontProperties(fname = '/Library/Fonts/microsoft/Fangsong.ttf')
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
        # print self.get_fund_code()
        #
        # print self.fund_rate()

# get fund code under condition selected
    def get_fund_code(self):

        fund_data = self.fund_data()[0]
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
        # self.fund_date = self.ui.fund_date.date().toPyDate()
        table_name = self.table_name()[0]
        sql_script = "select rate from %s where get_date = '%s' and code = '%s'" % (table_name, str(self.fund_data()[1]), fund_code)
        fund_rate = read(sql_script)
        fund_rate = '%.3f' % fund_rate.ix[0, 0]
        return fund_rate

# get all data from fund cal table in database
    def fund_data(self):
        table_name = self.table_name()[1]
        fund_date = self.ui.fund_date.date().toPyDate()
        # sql_script = "select * from %s where get_date = '%s'" % (table_name, fund_date)
        # fund_data_all = read(sql_script)
        condition = True
        while(condition):
            sql_script = "select * from %s where get_date = '%s'" % (table_name, fund_date)
            fund_data_all = read(sql_script)
            if (len(fund_data_all) == 0):
                fund_date = fund_date - timedelta(days = 1)
                self.ui.fund_date.setDate(fund_date)
            else:
                condition = False


        return (fund_data_all, fund_date)
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
        # self.ui.widget.canvas.mpl_connect('motion_notify_event', self.move_on)
        # self.ui.widget.canvas.setMouseTracking(True)
        self.ui.widget.canvas.installEventFilter(self)

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
        # get_date = self.ui.fund_date.date().toPyDate()
        fund_code = self.ui.fund_code.currentText()
        sql_script = "select stock_code, percent_net, percent_net_now from %s where get_date = '%s' and code = '%s'" % (table_name, self.fund_data()[1], fund_code)
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
        start_day = QtCore.QDate.addDays(input_day, -5).toPyDate()
        end_day = input_day.toPyDate()
        table_name = self.table_name()
        fund_code = self.ui.fund_code.currentText()

        draw_data_sql = "select code, stock_code, percent_net, percent_net_now, get_date from %s where code = '%s' and get_date>= '%s' and get_date < '%s'" % (table_name[1], fund_code, start_day, end_day)
        draw_data = read(draw_data_sql)
        xaxes_date = draw_data.get_date.drop_duplicates('get_date')
        bar_width = 0.35

        self.ui.widget.canvas.period_percent_rate.clear()
        self.ui.widget.canvas.period_percent_rate.set_title(u'top stocks rate changed ')
        self.ui.widget.canvas.period_percent_rate.xaxis.set_major_locator(MultipleLocator(10))
        # points_with_annotation = []
        index_with_annotation = []
        for i in draw_data.index:
            bar_com = self.ui.widget.canvas.period_percent_rate.bar(draw_data.index[i], draw_data.percent_net[i], bar_width, color = 'b', picker = 5)
            bar_cal = self.ui.widget.canvas.period_percent_rate.bar(draw_data.index[i] + bar_width, draw_data.percent_net_now[i], bar_width, color = 'y', picker = 5)


        self.ui.widget.canvas.period_percent_rate.legend([bar_com, bar_cal], ['compay', 'recal'])
        self.ui.widget.canvas.period_percent_rate.xaxis.grid(True, which='major')
        self.ui.widget.canvas.period_percent_rate.yaxis.grid(True)
        self.ui.widget.canvas.period_percent_rate.set_ylim(0, max(draw_data.percent_net_now)+max(draw_data.percent_net_now) * 0.2)
        self.ui.widget.canvas.period_percent_rate.set_xticklabels(['0'] + ['0'] + list(xaxes_date))
        self.ui.widget.canvas.draw()
        # print self.points_with_annotation
        # print draw_data
        # print self.points_with_annotation
        return (draw_data, index_with_annotation)

    # define mouse clicks events
    def on_pick(self, event):
        # ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
        global stock_code
        artist = event.artist
        x = artist.get_bbox().x0
        y = artist.get_bbox().y1
        my_data = self.draw_today_Pnet()
        stock_code = my_data[my_data.index == int(x)]['stock_code']
        stock_code = stock_code.ix[int(x), 0]
        self.text = self.ui.widget.canvas.period_percent_rate.text(x, y, u'stock_code: %s' % stock_code)
        # self.text.set_text("")
        self.ui.widget.canvas.draw()

        # return stock_code

    def offclick(self, event):
        try:
            self.text.remove()
            self.ui.widget.canvas.draw()
        except:
            pass
    def draw_stock_plot(self):
        stock_sql = "select buy, get_date from stock_data where code = '%s'" % stock_code
        print stock_sql
        stock_data = read(stock_sql)
        print stock_data
        figi = plt.figure()
        ax = figi.add_subplot(111)
        ax.plot(stock_data.buy)
        figi.show()
    def eventFilter(self, obj, event):

        if (event.type() == QtCore.QEvent.MouseButtonPress):
            self.ui.widget.canvas.mpl_connect('pick_event', self.on_pick)
        if (event.type() == QtCore.QEvent.MouseButtonDblClick):
            self.draw_stock_plot()
            # print stock_code

            # print "test"


    def move_on(self, event):

        for i in self.draw_today_Pnet()[0].index:
            if (i == int(event.xdata)):
                self.ui.widget.canvas.period_percent_rate.text(event.xdata, max(self.draw_today_Pnet()[0].percent_net[i]+1, self.draw_today_Pnet()[0].percent_net_now[i]+1), self.draw_today_Pnet()[0].stock_code[i], color = "red")
                self.ui.widget.canvas.draw()





def main():
    app = QtGui.QApplication(sys.argv)
    gui = GUIForm()
    gui.show()
    app.exec_()

if __name__ == "__main__":

    main()