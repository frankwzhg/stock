#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import op_database as op_db
from time import strftime, gmtime

# calculate creative fund rate
def cal_rate(fund_table, sk_table, cur_price):
    sel_date = strftime("%Y-%m-%d", gmtime())
    fund_table = op_db.read("select * from test." + fund_table + " where get_date =" + "'" + sel_date + "'")
    sk_table = op_db.read("select * from test." + sk_table + " where get_date =" + "'" + sel_date + "'")
    fund_table = fund_table[fund_table['code'].isin(sk_table['code'])]

    fund_creative_cal = fund_table[["code", "F_name", "F_net", "get_date"]].drop_duplicates()
    sk_table = sk_table[["code", cur_price]].drop_duplicates()
    fund_creative_cal = pd.merge(fund_creative_cal, sk_table, on="code")
    fund_creative_cal = fund_creative_cal.dropna()
    fund_creative_cal = fund_creative_cal[fund_creative_cal.F_net != ""]
    fund_creative_cal = fund_creative_cal[fund_creative_cal.F_net != "0"]
    fund_creative_cal = fund_creative_cal[fund_creative_cal[cur_price] != "0"]
    fund_creative_cal[['F_net', cur_price]] = fund_creative_cal[['F_net', cur_price]].astype(float)
    fund_creative_cal['rate'] = (fund_creative_cal[cur_price] - fund_creative_cal.F_net)/fund_creative_cal.F_net * 100
    # op_db.save(fund_creative_cal, "fund_creative_cal")
    return fund_creative_cal

if __name__ == "__main__":
    op_db.save(cal_rate("fund_creative_FD", "fund_creative_SK", "Cprice"), "fund_creative_rate")
    op_db.save(cal_rate("fund_Close_FD", "fund_Close_SK", "buy"), "fund_Close_rate")
    op_db.save(cal_rate("fund_ETF_FD", "fund_ETF_SK", "buy"), "fund_ETF_rate")
    op_db.save(cal_rate("fund_LOF_FD", "fund_LOF_SK", "buy"), "fund_LOF_rate")
    # print cal_rate("fund_Close_FD", "fund_Close_SK", "buy")
    # print cal_rate("fund_creative_FD", "fund_creative_SK", "Cprice")
    # print cal_rate("fund_ETF_FD", "fund_ETF_SK", "buy")
    # print cal_rate("fund_LOF_FD", "fund_LOF_SK", "buy")



