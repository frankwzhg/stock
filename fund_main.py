#! /usr/bin/python

import os.path
import op_database as op_db
from time import strftime, gmtime, sleep, localtime
import importlib

# load data for each module
sel_date = strftime("%Y-%m-%d", gmtime())

def run_module(module, table_name_list):
    for table_name in table_name_list:
        file_name = "/home/frank/stock/data/{0}_{1}.csv".format(table_name, sel_date)
        temp = op_db.read("select count(*) from test." + table_name + " where get_date =" + "'" + sel_date + "'")
        while ((temp.ix[0, 0] == 0) &(os.path.isfile(file_name) == False)):
            try:
                mod = importlib.import_module(module)
                mod.save_data(table_name)
                temp = op_db.read("select count(*) from test." + table_name + " where get_date= " + "'" + sel_date + "'")
                # sleep(300)
            except:
                sleep(60)
                temp.ix[0, 0] = 0
            # temp = op_db.read("select count(*) from test." + table_name + " where get_date= " + "'"
            # + sel_date + "'")
        print "moudule: " + module +" data frame: " + table_name + " is loaded sucessfully"

if __name__ == "__main__":

    close_date = ('2015-06-22', '2015-10-01', '2015-10-02', '2015-10-05', '2015-10-06', '2015-10-07')
    current_date = strftime("%A", localtime())
    today_date = strftime('%Y-%m-%d', gmtime())
    if any(today_date in code for code in close_date):
        quit()
    else:
        if any(current_date in code for code in close_date):
            quit()
        else:
            run_module("stock_data", ['stock_data'])
            run_module("fund_stock_close_ETF_LOF_sina", ['fund_Close_SK', 'fund_ETF_SK', 'fund_LOF_SK'])
            run_module("fund_close_ETF_LOF_sina", ['fund_Close_FD', 'fund_ETF_FD', 'fund_LOF_FD'])
            run_module("fund_creative_sina", ["fund_creative_SK", "fund_creative_FD"])
            run_module("fund_top_stock", ['fund_Close_top_stocks', 'fund_ETF_top_stocks', 'fund_LOF_top_stocks', 'fund_creative_top_stocks'])
            run_module("fund_information", ['fund_Close_FD_info', 'fund_ETF_FD_info', 'fund_LOF_FD_info', 'fund_creative_FD_info'])
            run_module("fund_cal_rate", ['fund_Close_rate', 'fund_ETF_rate', 'fund_LOF_rate', 'fund_creative_rate'])
            run_module("fund_data_recal", ['fund_Close_cal', 'fund_ETF_cal', 'fund_LOF_cal', 'fund_creative_cal'])


# if __name__ == "__main__":
#     run_module('/home/frank/stock/stock_data.py', ['stock_data'])
#     run_module('/home/frank/stock/fund_stock_close_ETF_LOF_sina.py', ['fund_Close_SK', 'fund_ETF_SK', 'fund_LOF_SK'])
#     run_module("/home/frank/stock/fund_close_ETF_LOF_sina.py", ['fund_Close_FD', 'fund_ETF_FD', 'fund_LOF_FD'])
#     run_module("/home/frank/stock/fund_creative_sina.py", ["fund_creative_SK", "fund_creative_FD"])
#     run_module('/home/frank/stock/fund_top_stock.py', ['fund_Close_top_stocks', 'fund_ETF_top_stocks', 'fund_LOF_top_stocks', 'fund_creative_top_stocks'])
#     run_module('/home/frank/stock/fund_information.py', ['fund_Close_FD_info', 'fund_ETF_FD_info', 'fund_LOF_FD_info', 'fund_creative_FD_info'])
#     run_module('/home/frank/stock/fund_cal_rate.py',['fund_Close_rate', 'fund_ETF_rate', 'fund_LOF_rate', 'fund_creative_rate'])
#     run_module('/home/frank/stock/fund_data_recal.py', ['fund_Close_cal', 'fund_ETF_cal', 'fund_LOF_cal', 'fund_creative_cal'])
#     # d = localtime()
#     # print strftime("%A", d)