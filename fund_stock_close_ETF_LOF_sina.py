#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import urllib2
import json
import op_database as op_db
from pandas.io.json import json_normalize
from time import strftime, gmtime, sleep

get_date = strftime("%Y-%m-%d", gmtime())
url_dic = {"fund_ETF_SK":"http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page={0}&num=40&sort=symbol&asc=0&node=etf_hq_fund&%5Bobject%20HTMLDivElement%5D=me540", "fund_Close_SK":"http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page={0}&num=40&sort=symbol&asc=0&node=close_fund&%5Bobject%20HTMLDivElement%5D=xsuqp", "fund_LOF_SK":"http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page={0}&num=40&sort=symbol&asc=0&node=lof_hq_fund&%5Bobject%20HTMLDivElement%5D=ycwtc"}

def get_fund_data_sina(url1):
    # print url1
    page_num = 1
    fund_data_df = pd.DataFrame()
    page = True
    while(page):
        loop_variable = True
        while(loop_variable):
            try:
                url = url1.format(page_num)
                # print url
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
                    loop_variable = False
            except:
                sleep(30)
                loop_variable = True
        if len(fund_df_tmp) == 40:
            page_num = page_num + 1
            # print page_num
            # url = url.format(page_num)
            # print url

        else:
            page = False
        fund_data_df = fund_data_df.append(fund_df_tmp)

    return fund_data_df

def save_data(table_name):
    url = url_dic.get(table_name)
    fund_stock_data = get_fund_data_sina(url)
    fund_stock_data["get_date"] = get_date
    try:
        op_db.save(fund_stock_data, table_name)
    except:
        fund_stock_data.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, get_date))
    return fund_stock_data



if __name__ == "__main__":

    # ETF_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=etf_hq_fund&%5Bobject%20HTMLDivElement%5D=me540")


    # print url_dic.get("fund_ETF_SK")
    print save_data("fund_Close_SK")

    # ETF_DF["get_date"] = get_date
    # Close_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=close_fund&%5Bobject%20HTMLDivElement%5D=xsuqp")
    # Close_DF["get_date"] = get_date
    # LOF_DF = get_fund_data_sina("http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['JVHWfRDKmSwbOcy1']/Market_Center.getHQNodeDataSimple?page=", 1, "&num=40&sort=symbol&asc=0&node=lof_hq_fund&%5Bobject%20HTMLDivElement%5D=ycwtc")
    # LOF_DF["get_date"] = get_date
    # op_db.save(ETF_DF, "fund_ETF_SK")
    # op_db.save(Close_DF, "fund_Close_SK")
    # op_db.save(LOF_DF, "fund_LOF_SK")


