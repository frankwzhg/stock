#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
this is get price of all A chinese stock. first, the 
"""
import json
import pandas as pd
import urllib2
from time import strftime, gmtime
import op_database as op_db
'''
"symbol" -- 股票全代码,"code" -- 代码,"name"-- 股票名称,"trade"--当前价格,"pricechange"--价格变化值,"changepercent"--价格变化率,"buy"--买入价,"sell" --卖出价,"settlement"--昨日收盘价,"open"--今日开盘价,"high"--今日最高价,"low"--今日最低价,"volume"--成交量,"amount"--成交额,"ticktime"--数据时间,"per"--,"per_d","nta"--每股净资产,"pb","mktcap","nmc","turnoverratio","favor","guba"
'''

# function "get_sz_stock_code" get shanghai and shengzhen stock code list from website. return varible stock_code_list
def stock_df_temp(pag_num):
    # stock_df_temp = pd.DataFrame()
    url = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0," + str(pag_num) + ",40]]&callback=FDC_DC.theTableData"
    # url = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,66,40]]&callback=FDC_DC.theTableData"
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    raw_data = res.read()
    # print raw_data
    raw_data = raw_data[70:-3]
    # print raw_data
    raw_data = json.loads(raw_data)
    # print len(raw_data["items"])
    # print pag_num
    stock_temp = pd.DataFrame()
    try:
        stock_temp = stock_temp.append(pd.DataFrame(raw_data["items"], columns=raw_data['fields']))
        stock_temp['get_date'] = strftime("%Y-%m-%d", gmtime())
    except:
        pass
    # print stock_temp
    # test = stock_temp
    return stock_temp

def save_data(tablename):
    pag_num = 1
    doit = True
    stock_df = pd.DataFrame()
    while (doit):
        # print len(stock_df_temp(pag_num))
        # print pag_num
        # print len(stock_df_temp(pag_num+1))
        stock_df = stock_df.append(stock_df_temp(pag_num))
        if len(stock_df_temp(pag_num)) == 40:
            pag_num = pag_num + 1
        else:
            doit = False
    op_db.save(stock_df, tablename)
    # return stock_df


if __name__ == "__main__":
    pag_num = 1
    doit = True
    stock_df = pd.DataFrame()
    while (doit):
        # print len(stock_df_temp(pag_num))
        # print pag_num
        # print len(stock_df_temp(pag_num+1))
        stock_df = stock_df.append(stock_df_temp(pag_num))
        if len(stock_df_temp(pag_num)) == 40:
            pag_num = pag_num + 1
        else:
            doit = False
    op_db.save(stock_df, "stock_data")
    # print stock_df
