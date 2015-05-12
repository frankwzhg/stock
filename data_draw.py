#!/usr/bin/python
# -*- coding: utf-8 -*-
from matplotlib.dates import datestr2num
import op_database as op_db
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
import datetime
temp_data = op_db.read("select * from test.fund_creative_rate")
temp_data.get_date = pd.to_datetime(pd.Series(temp_data.get_date))
# temp_data = temp_data[
# print temp_data.index in range(0,11,1)
# x = temp_data.index
# y = temp_data.rate
# z = temp_data.code[temp_data.index]


# bar(x, y, width=0.35)
# # ylim(10, 20)
# # xlim(1, 5)
# xticks(x, list(z))
# show()
# st = datetime.datetime(2015, 03, 27, 0, 0)
# en = datetime.datetime(2015, 03, 27, 0, 0)
ch_date = '2015-04-10'
time_data = temp_data[temp_data.get_date == ch_date]
print time_data
min_rate = 10
max_rate = 50
time_data = time_data[(time_data.rate>min_rate) & (time_data.rate<max_rate)]

time_data['get_date'] = pd.DatetimeIndex(time_data['get_date'])
# print temp_data
size = time_data.rate
subplot(211)
scatter(time_data.index, time_data.rate, s=size+10, c=size+20, alpha=0.5)
xticks(time_data.index, range(1, len(time_data.index), 1))
xlim(time_data.index[0]-1, time_data.index[-1]+2)
ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
# xlabel(u"从" + str(st.month) + u"月" + str(st.day) + u'到'+ str(en.month) + u"月" + str(en.day), fontproperties = ChineseFont1)
xlabel(ch_date)
for i in time_data.index:
    annotate(time_data.code[i], (i+2, time_data.rate[i]))

code = '150144'
code_data = temp_data[temp_data.code == code]
subplot(212)
plot(code_data.get_date, code_data.rate)
show()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ChineseFont1 = FontProperties(fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
# # ChineseFont2 = FontProperties('WenQuanYi')
#
# ax.plot(temp_data.get_date, temp_data.rate, '.')
# # plt.bar(temp_data.rate, temp_data.code)
# ax.set_title(u"这是测试", fontproperties = ChineseFont1)
# # ax.text(temp_data.get_date, temp_data.rate, u'这是另一个测试', fontproperties = ChineseFont1)
# xfmt = mdates.DateFormatter('%b %d')
# ax.xaxis.set_major_formatter(xfmt)
# for i in temp_data.index:
#     ax.annotate(temp_data.code[i], (temp_data.get_date[i], temp_data.rate[i]))
# # ax.axis([min(temp_data.get_date), max(temp_data.get_date), -20, 100], fontproperties = ChineseFont1)
# # plt.axes.text(temp_data.get_date, temp_data.rate, temp_data.code, fontproperties = ChineseFont1)
#
# plt.show()
