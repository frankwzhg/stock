#! /usr/bin/python

import os
import op_database as op_db
from time import strftime, gmtime, sleep, localtime
from stock_data import save_data

# load data for each module


def run_module(module, table_name_list):
    sel_date = strftime("%Y-%m-%d", gmtime())
    for table_name in table_name_list:
        temp = op_db.read("select count(*) from test." + table_name + " where get_date =" + "'" + sel_date + "'")
        while (temp.ix[0, 0] == 0):
            try:
                os.popen('python ' + module)
                temp = op_db.read("select count(*) from test." + table_name + " where get_date= " + "'" + sel_date + "'")
                # print temp.ix[0,0]
                sleep(30)
            except:
                temp.ix[0, 0] = 0
            # temp = op_db.read("select count(*) from test." + table_name + " where get_date= " + "'"
            # + sel_date + "'")
        print "moudule: " + module + " is loaded sucessfully"


if __name__ == "__main__":
    run_module('/home/frank/stock/stock_data.py', ['stock_data'])
    run_module('/home/frank/stock/fund_stock_close_ETF_LOF_sina.py', ['fund_Close_SK', 'fund_ETF_SK', 'fund_LOF_SK'])
    run_module("/home/frank/stock/fund_close_ETF_LOF_sina.py", ['fund_Close_FD', 'fund_ETF_FD', 'fund_LOF_FD'])
    run_module("/home/frank/stock/fund_creative_sina.py", ["fund_creative_SK", "fund_creative_FD"])
    run_module('/home/frank/stock/fund_top_stock.py', ['fund_Close_top_stocks', 'fund_ETF_top_stocks', 'fund_LOF_top_stocks', 'fund_creative_top_stocks'])
    run_module('/home/frank/stock/fund_information.py', ['fund_Close_FD_info', 'fund_ETF_FD_info', 'fund_LOF_FD_info', 'fund_creative_FD_info'])
    run_module('/home/frank/stock/fund_cal_rate.py',['fund_Close_rate', 'fund_ETF_rate', 'fund_LOF_rate', 'fund_creative_rate'])
    run_module('/home/frank/stock/fund_data_recal.py', ['fund_Close_cal', 'fund_ETF_cal', 'fund_LOF_cal', 'fund_creative_cal'])
    # d = localtime()
    # print strftime("%A", d)