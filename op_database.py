#!/usr/bin/python 
# -*- coding: utf-8 -*-

# import package
# import urllib2
# import pandas as pd
from pandas.io import sql
import MySQLdb


# save fund stock data into msysql database

def save(data_frame, tablname):
    db = MySQLdb.connect('frankub', 'root', 'Dadi4747', 'test', charset='utf8')                              #build mysql link
    sql.write_frame(data_frame, con=db, name=tablname, if_exists='append', flavor='mysql')
    db.close()
# read data from data base into a data Frame


def read(sql_script):
    db = MySQLdb.connect('frankub', 'root', 'Dadi4747', 'test', charset='utf8')
    my_data = sql.frame_query(sql_script, con=db)
    return my_data
    db.close()


# if __name__ == "__main__":
#     fund_data = read_dataDF("select * from test.fund_data;")
#     print fund_data
