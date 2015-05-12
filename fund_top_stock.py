#!/usr/bin/python 
# -*- coding: utf-8 -*-


import BeautifulSoup
import pandas as pd
import urllib2
import numpy as np
import op_database as op_db
from time import strftime, gmtime

"""
get top ten stock for each fund
"""
# # import fund_data_all dataframe
# sel_date = strftime("%Y-%m-%d", gmtime())
# # sel_date = '2015-02-11'
# fund_data = op_db.read("select * from test.fund_data where get_date =" + "'" + sel_date + "'")
# # fund_uncreative_data = fund_data[fund_data["F_code"].str.contains("150") == False]
# # get top stock and net information for each fund


def get_top_stock_each_fund(fund_code):
    url = "http://stock.finance.sina.com.cn/fundInfo/view/FundInfo_ZCGP.php?symbol=" + fund_code
    data = urllib2.urlopen(url).read()
    bs = BeautifulSoup.BeautifulSoup(data)
    top_stock = []
    for table in bs.findAll("tr", {"class": "f005"}):
        try:
            for line in table.findAll("td"):
                top_stock.append(line.text)
        except:
            pass
    try:
        top_stock = np.array(top_stock).reshape(len(top_stock) / 9, 9)
        top_stock = pd.DataFrame(top_stock)
        top_stock.columns = ["index_num", "stock_code", "stock_name", "keep_cur", "percent_net", "keep_stock_amount",
                             "percent_stock", "df_with_last", "keep_it_fundamount"]
        top_stock["F_code"] = fund_code
    except:
        pass
    # print top_stock
    return top_stock


# get top_stock and fund_net_company for each fund

def get_stock_net(fund_code_list):
    # print fund_code_list
    top_stock_allf_local = pd.DataFrame()
    for fund_code in fund_code_list.code:
        # print len(fund_code)
        stock = get_top_stock_each_fund(fund_code)
        top_stock_allf_local = top_stock_allf_local.append(stock)
    return top_stock_allf_local

# get fund data, and then split fund code
def get_fund_top_stocks(fund_name):
    sel_date = strftime("%Y-%m-%d", gmtime())
    fund_code = op_db.read("select code from test." + fund_name + "_FD where get_date =" + "'" + sel_date + "'")
    # print 'fund_code ' + fund_code
    fund_stock_code = op_db.read("select code from test." + fund_name + "_SK where get_date=" + "'" + sel_date + "'")
    # print 'fund_stock_code ' + fund_stock_code
    fund_code = fund_code[fund_code['code'].isin(fund_stock_code.code)]
    top_stock = get_stock_net(fund_code)
    top_stock['get_date'] = sel_date
    return top_stock
if __name__ == "__main__":
    for fund in ["fund_Close", "fund_ETF", "fund_LOF", "fund_creative"]:
        stocks = get_fund_top_stocks(fund)
        # print stocks
        op_db.save(stocks, fund + '_top_stocks')
    # print get_fund_top_stocks("fund_Close")
    # print top_stock_allF
