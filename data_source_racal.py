#!/usr/bin/python 
# -*- coding: utf-8 -*-

import op_database as op_db
import re
import pandas as pd
from time import gmtime, strftime

# get related data from data frame


def get_df_for_day(recal_date):
    fund_data_local = op_db.read("select * from test.fund_data where get_date =" + "'" + recal_date + "'")
    top_stock_local = op_db.read("select * from test.top_stock where get_date =" + "'" + recal_date + "'")
    stock_data_local = op_db.read("select * from test.stock_data where Date =" + "'" + recal_date + "'")
    fund_information_local = op_db.read("select * from test.fund_information where get_date =" + "'" + recal_date + "'")
    return fund_data_local, top_stock_local, stock_data_local, fund_information_local
# fund_data, top_stock, stock_data, fund_information = get_df_for_day(recal_day)
# adjust fund_information dataframe, convert number value to float, and convert percentage to float
# delete date and bracket in F_Tamount and F_Tvalue field


def del_date_str(DF, old_colname, new_colname):
    col_value = []
    for value in DF[old_colname]:
        col_value.append(re.split(' ', value)[0])
    col_value = pd.DataFrame(col_value, columns=[new_colname])
    DF = DF.join(col_value)
    DF[new_colname] = DF[new_colname].astype(float)
    # DF[new_colname][DF[new_colname] == "--"] = "0%"
    # #DF.F_Dmanagement[DF["F_Dmanagement"] == "--"] = "0%"
    # DF[new_colname] = DF[new_colname].str.rstrip('%').astype(float) / 100
    return DF

# percent symbol from dataframe field


def del_perc_str(DF, old_colname, new_colname):
    DF[old_colname][DF[old_colname] == "--"] = "0%"
    DF[new_colname] = DF[old_colname].str.rstrip('%').astype(float) / 100
    return DF
# fund_information = del_date_str(fund_information, "F_Tvalue", "F_TVal")

# ###filter uncreative fund from fund_data
# fund_data = fund_data[fund_data["F_code"].str.contains("150") == False]

# get F_code F_net and F_TAmut from fund_data, and F_code and F_TVal from fund_information
# and then merge this sub dataframe. get source ####dataframe
# data_source = pd.merge(fund_data[["F_code", "F_net", "F_date_net", "F_Tamount"]],
# fund_information[["F_code", "F_TVal"]], on = "F_code", how = 'left')

# ###merge stock_code, stock_name, keep_cur, keep_stock_amount, F_code from top_stock
# data_source = pd.merge(data_source, top_stock[["F_code", "stock_code", "stock_name", "keep_cur", "keep_stock_amount",
# "percent_net"]], on = "F_code", how = 'left')

# get YCprice, Date, Code from stock_data, and them merge sub stock_data into data_source and by stock_code
# stock_data["stock_code"] = stock_data.Code.map(lambda x : x[2:])
# data_source = pd.merge(data_source, stock_data[["stock_code","YCprice", "Date"]])
if __name__ == "__main__":
    recal_day = strftime("%Y-%m-%d", gmtime())
    # recal_day = '2015-01-29'
    # print recal_day
    fund_data, top_stock, stock_data, fund_information = get_df_for_day(recal_day)
    # if (len(fund_data) == 0 and len(top_stock) == 0 and len(stock_data) == 0 and len(fund_information) == 0):
    test = [len(fund_data), len(top_stock), len(stock_data), len(fund_information)]
    if all([v == 0 for v in test]):
        print "sorry, you have not right dataframe to recal"
    else:
        # print fund_data
        fund_information = del_date_str(fund_information, "F_Tvalue", "F_TVal")

        # filter uncreative fund from fund_data
        # fund_data = fund_data[fund_data["F_code"].str.contains("150") == False]

        # get F_code F_net and F_TAmut from fund_data, and F_code and F_TVal from fund_information and then merge
        # this sub dataframe. get source ####dataframe
        data_source = pd.merge(fund_data[["F_code", "F_net", "F_date_net", "F_Tamount"]],
                               fund_information[["F_code", "F_TVal"]], on="F_code", how='left')

        # merge stock_code, stock_name, keep_cur, keep_stock_amount, F_code from top_stock
        data_source = pd.merge(data_source, top_stock[["F_code", "stock_code", "stock_name", "keep_cur",
                                                       "keep_stock_amount", "percent_net"]], on="F_code", how='left')

        # get YCprice, Date, Code from stock_data, and them merge sub stock_data into data_source and by stock_code
        stock_data["stock_code"] = stock_data.Code.map(lambda x: x[2:])
        data_source = pd.merge(data_source, stock_data[["stock_code", "YCprice", "Date"]])
        # print data_source
        op_db.save(data_source, "data_source")