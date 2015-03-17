#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
this is get price of all A chinese stock. first, the 
"""
# import json
# import requests
# import BeautifulSoup
import pandas as pd
# from pandas.io import sql
# import MySQLdb
import urllib2
# import numpy as np
# import datetime
import op_database as op_db

# function "get_sz_stock_code" get shanghai and shengzhen stock code list from website. return varible stock_code_list


def get_sz_stock_code():
    stock_code_list = []
    for p_num in range(1, 60):
        url = "http://stock.gtimg.cn/data/index.php?appn=rank&t=ranka/chr&p=" + str(p_num) + "&o=0&l=40&v=list_data"
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        raw_data = res.read()
        stock_code = raw_data[57:-3]
        stock_code = stock_code.split(",")
        # stock_code = json.loads(stock_code)
        stock_code_list = stock_code_list + stock_code
    return stock_code_list

# base on stock_code_list, create stock url on sina finance website for each stock code


def stock_url_create(stock_code_list):
    stock_url_list = []
    for code in stock_code_list:
        url = "http://hq.sinajs.cn/list=" + code.strip("'")
        stock_url_list.append(url)
    return stock_url_list

# get stock data from sina website following url list for each stock code, return stock data dataframe


def stock_data_get(stock_url_list):
    stock_data = []
    for url in stock_url_list:
        # code = code.strip('f')
        # url = "http://hq.sinajs.cn/list=sz" + code
        # print url
    
        # url = "http://hq.sinajs.cn/list=sz150158"
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        htm = res.read()
        res.close()
        htm = htm[21:-3]
        htm = url[-8:] + "," + htm
        htm = unicode(htm, "gb2312").encode("utf8")
        htm = htm.split(",")
        stock_data.append(htm)
        stock_fdata_local = pd.DataFrame(stock_data)
        stock_fdata_local = stock_fdata_local[range(0, 9)+range(31, 33)]
        stock_fdata_local.columns = ["Code", "Name", "TOprice", "YCprice", "Cprice", "THprice", "TLprice", "DealData",
                                     "DealAmout", "Date", "Time"]
    return stock_fdata_local
# get all stock data and create stock data dataframe


def stock_fdata():
    stock_code_list = get_sz_stock_code()
    stock_url_list = stock_url_create(stock_code_list)
    stock_fdata_local = stock_data_get(stock_url_list)
    return stock_fdata_local


if __name__ == "__main__":
    stock_fdata = stock_fdata()
    # print stock_fdata
    op_db.save(stock_fdata, "stock_data")
