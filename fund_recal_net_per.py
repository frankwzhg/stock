#! /usr/bin/python
# -*- coding: utf-8 -*-

import op_database as op_db
# import re
import pandas as pd
import numpy as np
from time import strftime, gmtime


def get_ds_recal_day(recal_date):
    data_source_local = op_db.read("select * from test.data_source where Date =" + "'" + recal_date + "'")
    data_source_local["keep_stock_amount"] = data_source_local.keep_stock_amount.map(lambda x: x.replace(',', ''))
    data_source_local["keep_cur"] = data_source_local.keep_cur.map(lambda x: x.replace(',', ''))
    data_source_local[['F_net', 'F_Tamount', 'keep_cur', 'keep_stock_amount', 'YCprice', 'percent_net']] = \
        data_source_local[['F_net', 'F_Tamount', 'keep_cur', 'keep_stock_amount', 'YCprice', 'percent_net']].astype(
            float)
    return data_source_local


# recalculate F_TVal_new,


def recal_f_tval(fund_code):
    temp_df_local = data_source[data_source["F_code"] == fund_code]
    temp_df_local["F_TCVal"] = sum(temp_df_local.keep_cur / (temp_df_local.percent_net / 100)) / len(temp_df_local)
    temp_df_local["F_Tamount_now"] = temp_df_local.F_TVal / temp_df_local.F_net
    temp_df_local["percent_net_now"] = ((temp_df_local.keep_stock_amount * temp_df_local.YCprice) / (temp_df_local.F_TVal * 100000000)) * 100
    temp_df_local["percent_net_Csum"] = sum(temp_df_local.percent_net)
    temp_df_local["percent_net_Nsum"] = sum(temp_df_local.percent_net_now)
    # temp_df["F_net_top_C"] = sum(temp_df.keep_cur)/(temp_df.F_Tamount * 100000000)
    # temp_df["F_net_top_N"] = sum(temp_df.keep_stock_amount * temp_df.YCprice)/(temp_df.F_Tamount * 100000000)
    return temp_df_local
    # df["F_TVal_new"] = df.keep_cur)


if __name__ == "__main__":
    recal_day = strftime("%Y-%m-%d", gmtime())
    # recal_day = "2015-01-29"
    data_source = get_ds_recal_day(recal_day)
    F_code_list = data_source.F_code.unique()
    if (len(data_source) == 0):
        print "you have not right dataframe to recalculate"
    else:
        data_source_recal = pd.DataFrame()
        for F_code in F_code_list:
            # print F_code
            temp_df = recal_f_tval(F_code)
            data_source_recal = data_source_recal.append(temp_df)
        data_source_recal = data_source_recal.replace([np.inf, -np.inf], np.nan).dropna()
        # print data_source_recal[data_source_recal.F_code == '169101']
        # print data_source_recal[data_source_recal.percent_net == 0]
        # print data_source_recal
        op_db.save(data_source_recal, "data_source_recal")