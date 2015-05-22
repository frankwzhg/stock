#!/usr/bin/python 
# -*- coding: utf-8 -*-
# import json
# import requests
from bs4 import BeautifulSoup
import pandas as pd
# from pandas.io import sql
# import MySQLdb
import urllib2
import numpy as np
import op_database as op_db
from time import strftime, gmtime, sleep
# import recalcuate_fund_net as re_cal


# print fund_LOF_code
# fund_uncreative_data = fund_data_all[fund_data_all["F_code"].str.contains("150") == False]
"""
get fund basic and management information, and then create fund_information dataframe, and also save it into database
table named fund_information
"""

# get fund basic information
sel_date = strftime("%Y-%m-%d", gmtime())

def fund_basic_information(basic_url):
    loop_variable = True
    while(loop_variable):
        try:
            raw_data = urllib2.urlopen(basic_url).read()
            bs = BeautifulSoup(raw_data)
            cont = []
            for div in bs.findAll("div", {"class": "tableContainer"}):
                print div
                for span in div.findAll("span"):
                    cont.append(span.text)
            fund_basic_data_info = pd.DataFrame(np.array(cont[2:42]).reshape(20, 2))  # , columns=["item","value"])
            loop_variable = False
        except:
            sleep(60)
            loop_variable = True
    return fund_basic_data_info


# get fund management information

def fund_management_information(mg_url):
    loop_variable = True
    while(loop_variable):
        try:
            raw_data = urllib2.urlopen(mg_url).read()
            print "raw_data", raw_data
            bs = BeautifulSoup(raw_data)
            cont = []
            for table in bs.findAll("table", {"class": "tc ntb"}):
                for td in table.findAll('td'):
                    cont.append(td.text)
            fund_management_information_local = pd.DataFrame(np.reshape(cont[:6], (2, 3)))
            fund_management_information_local = fund_management_information_local.T
            loop_variable = False
        except:
            sleep(60)
            loop_variable = True
    return fund_management_information_local

# merge fund basic information and management information into one dataframe fund_information
# filed name
"""
## F_name = 基金简称, F_code = 基金代码, C_date = 成立日期, S_date = 上市日期, K_years = 存续期限(年), S_location = 上市地点
##F_Tamount = 基金总份额(亿份), F_Samount = 上市流通份额(亿份), F_Tvalues = 基金规模(亿元), Stock_style = 选股风格, F_owner = 基金管理人,
##F_Dmanager = 基金托管人, F_manager = 基金经理, OP_style = 运作方式, F_type = 基金类型, Sec_cat = 二级分类, S_agent1 = 代销机构(银行）,
##S_agent2 = 代销机构(证劵), Min_Bvalue = 最低参与金额(元), Min_Bamount = 最低赎回份额(份), F_Fmanagement = 基金管理费, F_Sservice = 销售服务费
"""


def fund_infor_data(fund_code):
    # loop_variable = True
    # while(loop_variable):
    #     try:
    basic_url = "http://stock.finance.sina.com.cn/fundInfo/view/FundInfo_JJGK.php?symbol={0}".format(fund_code)
    mg_url = "http://stock.finance.sina.com.cn/fundInfo/view/FundInfo_JJFL.php?symbol={0}".format(fund_code)
    print basic_url
    fund_basic_data = fund_basic_information(basic_url)
    fund_management_data = fund_management_information(mg_url)
    fund_information_local = fund_basic_data.append(fund_management_data).T
    fund_information_local.columns = ["F_name", "F_code", "C_date", "S_date", "K_years", "S_location", "F_Tamount",
                                "F_Samount", "F_Tvalue", "Stock_style", "F_owner", "F_Dmanager", "F_manager",
                                "OP_style", "F_type", "Sec_cat", "S_agent1", "S_agent2", "Min_Bvalue", "Min_Bamount",
                                "F_Fmanagement", "F_Dmanagement", "F_Sservice"]
        #     loop_variable = False
        # except:
        #     loop_variable = True
    return fund_information_local
#
#
# # get all fund information, and then create fund_information dataframe by fund code in fund_data

def fund_information(fund):
    fund_infor = pd.DataFrame()
    for code in fund.code:
        print code
        fund_infor = fund_infor.append(fund_infor_data(str(code))[1:])
        print "fund_infor", fund_infor
    return fund_infor

# get fund data from database and get fund information from website
def get_fund_info(fund_name):

    fund_tmp = op_db.read("select * from test.{0} where get_date ='{1}'".format(fund_name, sel_date))
    fund_info_tmp = fund_information(fund_tmp)
    print "fund_info_tmp", fund_info_tmp
    fund_info_tmp['get_date'] = sel_date

    return fund_info_tmp
    # op_db.save(fund_info_tmp, fund_name + "_info")

def save_data(table_name):
    fund_name = table_name[:-5]
    print fund_name
    fund_info = get_fund_info(fund_name)
    print "fund_info", fund_info
    try:
        op_db.save(fund_info, table_name)
        print "adb"
    except:
        print "ddf"
        fund_info.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, sel_date))
    return fund_info

if __name__ == "__main__":

    # print fund_basic_information("http://stock.finance.sina.com.cn/fundInfo/view/FundInfo_JJGK.php?symbol=512990")  #512990")
    # print fund_infor_data("512990")
    print save_data("fund_Close_FD_info")
    # for fund in ["fund_Close_FD", "fund_ETF_FD", "fund_creative_FD", "fund_LOF_FD"]:
    #     get_fund_info(fund)
    # get_fund_info("fund_LOF")