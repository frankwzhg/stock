#!/usr/bin/python
# -*- coding: utf-8 -*-


import op_database as op_db
from time import gmtime, strftime
import pandas as pd
import numpy as np


# calculate fund total vaule(基金当前总市值）, 计算方式是用基金中的top ten股票的每只股票当前市值除以基金净值比的平均值
def cal_total_value(fund_name):
    fund = op_db.read("select * from test." + fund_name + "_top_stocks") # where get_date = " + "'" + strftime("%Y-%m-%d", gmtime()) + "'")
    # print fund
    fund["keep_cur"] = fund.keep_cur.map(lambda x: x.replace(',', ''))
    fund["keep_stock_amount"] = fund.keep_stock_amount.map(lambda x: x.replace(',', ''))
    fund[['keep_cur', 'percent_net', 'keep_stock_amount']] = fund[['keep_cur', 'percent_net', 'keep_stock_amount']].astype(float)
    fund_code_list = fund.F_code.drop_duplicates()
    fund_cal = pd.DataFrame()
    # print fund_cal
    for code in fund_code_list:
        fund_temp = fund[fund.F_code == code].copy()
        fund_temp["F_TCVal"] = sum(fund_temp.keep_cur/(fund_temp.percent_net/100))/len(fund_temp)/100000000
        # print fund_cal
        fund_cal = fund_cal.append(fund_temp)
    fund_cal = fund_cal.rename(columns = {"F_code":"code"})
    return fund_cal
#
if __name__ == "__main__":
    for fd in ["fund_creative", "fund_Close", "fund_ETF", "fund_LOF"]:
        temp = cal_total_value(fd)
        temp = temp[np.isfinite(temp["F_TCVal"])]
        fund_data = op_db.read("select F_net, code from test." + fd + "_FD") # where get_date=" + "'" + strftime('%Y-%m-%d', gmtime()) + "'")
        fund_data = fund_data[fund_data['F_net'] != '']
        fund_data['F_net'] = fund_data['F_net'].astype(float)
        fund_cal = pd.merge(temp, fund_data, on="code")
        fund_cal["F_Tamount_now"] = fund_cal.F_TCVal/fund_cal.F_net
        stock_data = op_db.read("select * from test.stock_data") # where get_date = " + "'"+ strftime("%Y-%m-%d", gmtime()) + "'")
        stock_data = stock_data[stock_data.code.isin(fund_cal.stock_code)]
        stock_data = stock_data[["code", "buy"]]
        stock_data = stock_data.rename(columns = {"code":"stock_code"})
        stock_data.buy = stock_data.buy.astype(float)
        # print stock_data[np.isnan(stock_data.buy)]
        fund_cal = pd.merge(fund_cal, stock_data, on="stock_code", how="left")

        fund_cal["percent_net_now"] = fund_cal.keep_stock_amount * fund_cal.buy/fund_cal.F_TCVal/1000000
        per_net_temp = fund_cal.groupby(['code']).percent_net.sum()
        per_net_now_temp = fund_cal.groupby(['code']).percent_net_now.sum()
        per_net_temp = pd.DataFrame(per_net_temp)
        per_net_temp["code"] = per_net_temp.index
        per_net_temp = per_net_temp.rename(columns = {"percent_net":"percent_net_Csum"})
        per_net_now_temp = pd.DataFrame(per_net_now_temp)
        per_net_now_temp["code"] = per_net_now_temp.index
        per_net_now_temp = per_net_now_temp.rename(columns = {"percent_net_now":"percent_net_Nsum"})
        # print per_net_temp[0:1]
        fund_cal = pd.merge(fund_cal, per_net_temp, on="code", how="left")
        fund_cal = pd.merge(fund_cal, per_net_now_temp, on="code", how="left")
        fund_cal = fund_cal.replace("NaN", 0)
        # print fund_cal
        # print fund_cal[np.isnan(fund_cal.percent_net_now)]
        # print len(fund_cal.code.drop_duplicates())
        op_db.save(fund_cal, fd + "_cal")
