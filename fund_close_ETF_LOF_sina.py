#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import op_database as op_db
from time import strftime, gmtime, sleep

sel_date = strftime("%Y-%m-%d", gmtime())
def get_creative_fund(code):
    loop_variable = True
    while(loop_variable):
        try:
            url = "http://hq.sinajs.cn/rn=ry1yo&list=" + code
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            raw_data = unicode(res.read(), "GB2312")
            raw_data = raw_data[21:-3] + "," + code[2:]
            raw_data = raw_data.split(",")
            loop_variable = False
        except:
            sleep(30)
            loop_variable = True
    return raw_data

def get_fund_stock(fund_name):
    loop_variable = True
    table_name = fund_name[:-3]
    while(loop_variable):
        try:
            fund_temp = op_db.read("select * from test.{0}_SK where get_date = '{1}'".format(table_name, sel_date))
            stock_list = []
            for symbol in fund_temp.symbol:
                tmp_list = get_creative_fund('f_' + symbol[2:])
                stock_list.append(tmp_list)
            temp_DF = pd.DataFrame(stock_list)
            temp_DF.columns = ["F_name", "F_net", "F_Tnet", "B_D_net", "F_date_net", "F_Tamount", "code"]
            temp_DF['get_date'] = strftime('%Y-%m-%d', gmtime())
            loop_variable = False
        except:
            sleep(30)
            loop_variable = True
    return temp_DF

def save_data(table_name):
        fund_data = get_fund_stock(table_name)
        try:
            op_db.save(fund_data, table_name)
        except:
            fund_data.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, sel_date))
        return fund_data
if __name__ == "__main__":

    for fund in ["fund_Close_FD", "fund_ETF_FD", "fund_LOF_FD"]:
        temp_DF = get_fund_stock(fund)
        # op_db.save(temp_DF, fund[:-3] + "_FD")
        print temp_DF
# print fund_Close_FD.symbol