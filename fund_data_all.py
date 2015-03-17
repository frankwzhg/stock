#!/usr/bin/python 
# -*- coding: utf-8 -*-
import json
from time import gmtime, strftime
# import BeautifulSoup
import pandas as pd
# from pandas.io import sql
# import MySQLdb
import urllib2
# import numpy as np
# import datetime
import op_database as op_db

"""
get fund data from ijin website
"""

# get fund code follow website url given


def fund_code_get(url):
    raw_response = urllib2.urlopen(url).read()
    raw_response = raw_response.strip("'g()'")
    page_content = json.loads(raw_response)
    fund_code_list = page_content["data"]["data"].keys()
    return fund_code_list


# create fund_url and fund_stock url in order to get stock data from sina


def fund_url_create(url_list):
    # url = "http://fund.ijijin.cn/data/Net/fbs/cxx_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html"
    fund_code_list = []
    for url in url_list:
        fund_code_list = fund_code_list + fund_code_get(url)
    fund_url_list_local = []
    for code in fund_code_list:
        code = code.strip('f')
        fund_url_local = "http://hq.sinajs.cn/list=f_" + code
        # sub_code = code[0:2]
        # if(sub_code=="51" or sub_code == "50"):
        # url = "http://hq.sinajs.cn/list=sh" + code
        # else:
        #     url = "http://hq.sinajs.cn/list=sz" + code
        # url_list.append(url)
        fund_url_list_local.append(fund_url_local)
    return fund_url_list_local
    # url_list = [str(x) for x in url_list]
    # fund_url_list = [str(x) for x in fund_url_list]
    # return (url_list, fund_url_list)


# get fund_data_all


def fund_data_all(fund_url_list_local):
    data_list = []
    for fund_url_local in fund_url_list_local:
        raw_data = urllib2.urlopen(fund_url_local).read()[21:-3].decode('GB2312')
        raw_list = raw_data.split(",") + [fund_url_local[-6:]]
        data_list = data_list + [raw_list]
    return pd.DataFrame(data_list,
                        columns=["F_name", "F_net", "F_Tnet", "B_D_net", "F_date_net", "F_Tamount", "F_code"])

# get stock data related to each fund using stock_data_get function in stock data module by stock url.

if __name__ == "__main__":
    fund_url = ["http://fund.ijijin.cn/data/Net/fbs/cxx_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html",
                "http://fund.ijijin.cn/data/Net/fbs/ctx_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html",
                "http://fund.ijijin.cn/data/Net/info/ETF_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html",
                "http://fund.ijijin.cn/data/Net/info/LOF_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html"]
    fund_url_list = fund_url_create(fund_url)
    fund_data = fund_data_all(fund_url_list)
    fund_data['get_date'] = strftime("%Y-%m-%d", gmtime())
    # print fund_data
    op_db.save(fund_data, "fund_data")
    # fund_data.to_csv("fund_data.csv")




