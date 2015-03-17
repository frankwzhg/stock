#! /usr/bin/python

import os
import op_database as op_db
from time import strftime, gmtime, sleep

# load data for each module


def run_module(module, table_name, table_column):
    sel_date = strftime("%Y-%m-%d", gmtime())
    temp = op_db.read("select count(*) from test." + table_name + " where " + table_column + "=" + "'" + sel_date + "'")
    # print "select count(*) from test." + table_name + " where " + table_column + "=" + "'" + sel_date + "'"
    while (temp.ix[0, 0] == 0):
        try:
            os.popen('python ' + module)
            sleep(30)
            temp = op_db.read("select count(*) from test." + table_name + " where " + table_column + "=" + "'" + sel_date + "'")
        except:
            temp.ix[0, 0] = 0
        # temp = op_db.read("select count(*) from test." + table_name + " where " + table_column + "=" + "'"
        # + sel_date + "'")
    print "moudule: " + module + " is loaded sucessfully"


if __name__ == "__main__":
    run_module('stock_data.py', 'stock_data', 'Date')
    run_module('fund_data_all.py', 'fund_data', 'get_date')
    run_module('fund_top_stock.py', 'top_stock', 'get_date')
    run_module('fund_information.py', 'fund_information', 'get_date')
    run_module('data_source_racal.py', 'data_source', 'Date')
    run_module('fund_recal_net_per.py', 'data_source_recal', 'Date')
