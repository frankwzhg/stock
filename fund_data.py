#! /usr/bin/python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import pandas as pd

url = 'http://stock.finance.sina.com.cn/fundInfo/view/FundInfo_LSJZ.php?symbol=184722'
raw_data = urllib2.urlopen(url).read()
bs_data = BeautifulSoup(raw_data)
fund_data = bs_data.findAll("div", {"class":"box-hq"})

for th in fund_data:
    th_data = th.findAll('th')
# th_list =[]
# th_list.append(th_data[5])
# th_list.append(th_data[7:11])
data_list =[]
for i in (5,7,8,9,10):
    string_data = th_data[i].text
    string_data = string_data.split(':')
    # print string_data[1].rstrip()
    data_list.append(string_data[1].rstrip())

data_fund_info = pd.DataFrame(data_list).T
print data_fund_info
# per_net
# data_fund_info.columns = ["per_net"]
# print th_data[5].text
# print th_list[3].text
# print th_data[8].text
# print th_data[9].text
# print th_data[10].text



