#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import op_database as op_db
from time import strftime, gmtime

def get_creative_fund(code):
    url = "http://hq.sinajs.cn/rn=ry1yo&list=" + code
    # print url
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    raw_data = unicode(res.read(), "GB2312")
    # print type(code)
    raw_data = raw_data[21:-3] + "," + code[2:]
    # print raw_data
    raw_data = raw_data.split(",")
    # print code[2:0]
    # raw_data = raw_data.append(code[2:])
    # print raw_data
    # raw_data_df = pd.DataFrame(raw_data)
    return raw_data

def get_fund_stock(fund_name):
    sel_date = strftime("%Y-%m-%d", gmtime())
    fund_temp = op_db.read("select * from test." + fund_name + " where get_date =" + "'" + sel_date + "'")
    stock_list = []
    for symbol in fund_temp.symbol:
        tmp_list = get_creative_fund('f_' + symbol[2:])
        stock_list.append(tmp_list)
    temp_DF = pd.DataFrame(stock_list)
    temp_DF.columns = ["F_name", "F_net", "F_Tnet", "B_D_net", "F_date_net", "F_Tamount", "code"]
    temp_DF['get_date'] = strftime('%Y-%m-%d', gmtime())
    return temp_DF


if __name__ == "__main__":

    for fund in ["fund_Close_SK", "fund_ETF_SK", "fund_LOF_SK"]:
        temp_DF = get_fund_stock(fund)
        op_db.save(temp_DF, fund[:-3] + "_FD")
        # print temp_DF
# print fund_Close_FD.symbol