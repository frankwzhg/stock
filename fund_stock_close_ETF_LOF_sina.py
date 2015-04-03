#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import urllib2
import json
import op_database as op_db
from pandas.io.json import json_normalize
from time import strftime, gmtime

def get_fund_data_sina(url_first, page_num, url_last):
    fund_data_df = pd.DataFrame()

    page = True
    while(page):
        url = url_first + str(page_num) + url_last
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        raw_data = res.read()
        fund_data = raw_data[99:-2]
        word_list = ["symbol", "name", "trade", "pricechange", "changepercent", "buy", "sell", "settlement", "open", "high", "low", "volume", "amount", "code", "ticktime", "get_date"]
        for word in word_list:
            fund_data = fund_data.replace(word, '"' + word +'"')
        fund_data = fund_data.split("},")
        fund_df_tmp = pd.DataFrame()
        for list in fund_data:
            list = list + "}"
            list = list.replace("}}", "}")
            list_json = json.loads(unicode(list, "GB2312"))
            list_DF = json_normalize(list_json)
            fund_df_tmp = fund_df_tmp.append(list_DF)
        if len(fund_df_tmp) == 40:
            page_num = page_num + 1
        else:
            page = False
        fund_data_df = fund_data_df.append(fund_df_tmp)

    return fund_data_df


if __name__ == "__main__":
    get_date = strftime("%Y-%m-%d", gmtime())
    ETF_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=etf_hq_fund&%5Bobject%20HTMLDivElement%5D=me540")
    ETF_DF["get_date"] = get_date
    Close_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=close_fund&%5Bobject%20HTMLDivElement%5D=xsuqp")
    Close_DF["get_date"] = get_date
    LOF_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=lof_hq_fund&%5Bobject%20HTMLDivElement%5D=ycwtc")
    LOF_DF["get_date"] = get_date
    op_db.save(ETF_DF, "fund_ETF_SK")
    op_db.save(Close_DF, "fund_Close_SK")
    op_db.save(LOF_DF, "fund_LOF_SK")

