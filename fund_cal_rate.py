#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import op_database as op_db
from time import strftime, gmtime
sel_date = strftime("%Y-%m-%d", gmtime())
# sel_date = '2015-05-25'
# calculate creative fund rate
def cal_rate(fund_table, sk_table):
    fund_table = op_db.read("select * from test.{0} where get_date = '{1}'".format(fund_table, sel_date))
    print fund_table
    sk_table = op_db.read("select * from test.{0} where get_date = '{1}'".format(sk_table, sel_date))
    sk_table.rename(columns={'Cprice':'buy'}, inplace=True)
    fund_table = fund_table[fund_table['code'].isin(sk_table['code'])]
    fund_table = fund_table[["code", "F_name", "F_net", "get_date"]].drop_duplicates()
    sk_table = sk_table[["code", "buy"]].drop_duplicates()
    fund_cal = pd.merge(fund_table, sk_table, on="code")
    fund_cal = fund_cal.dropna()
    fund_cal = fund_cal[fund_cal.F_net != ""]
    fund_cal = fund_cal[fund_cal.F_net != "0"]
    fund_cal = fund_cal[fund_cal["buy"] != "0"]
    fund_cal[['F_net', "buy"]] = fund_cal[['F_net', "buy"]].astype(float)
    fund_cal['rate'] = (fund_cal["buy"] - fund_cal.F_net)/fund_cal.F_net * 100
    # op_db.save(fund_creative_cal, "fund_creative_cal")
    return fund_cal
def save_data(table_name):
    fund_name = table_name[:-5]
    fund_rate = cal_rate(fund_name + "_FD", fund_name + "_SK")
    try:
        # print "test"
        op_db.save(fund_rate, table_name)
    except:
        fund_rate.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, sel_date))

    return fund_rate

if __name__ == "__main__":
    print save_data("fund_ETF_rate")
    # print cal_rate("fund_Close_FD", "fund_Close_SK")
    # op_db.save(cal_rate("fund_creative_FD", "fund_creative_SK", "Cprice"), "fund_creative_rate")
    # op_db.save(cal_rate("fund_Close_FD", "fund_Close_SK", "buy"), "fund_Close_rate")
    # op_db.save(cal_rate("fund_ETF_FD", "fund_ETF_SK", "buy"), "fund_ETF_rate")
    # op_db.save(cal_rate("fund_LOF_FD", "fund_LOF_SK", "buy"), "fund_LOF_rate")
    # print cal_rate("fund_Close_FD", "fund_Close_SK", "buy")
    # print cal_rate("fund_creative_FD", "fund_creative_SK", "Cprice")
    # print cal_rate("fund_ETF_FD", "fund_ETF_SK", "buy")
    # print cal_rate("fund_LOF_FD", "fund_LOF_SK", "buy")



