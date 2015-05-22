#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from time import strftime, gmtime
import urllib2
import op_database as op_db

get_date = strftime('%Y-%m-%d', gmtime())

def split_fund_stock():
    fund_string = "f_150144,sz150144,f_150050,sz150050,f_150165,sz150165,f_150165,sz150165,f_150178,sz150178,f_162308,sz162308,f_150142,sz150142,f_150142,sz150142,f_150206,sz150206,f_150139,sz150139,f_150111,sz150111,f_150141,sz150141,f_150172,sz150172,f_150122,sz150122,f_150201,sz150201,f_150029,sz150029,f_150033,sz150033,f_150069,sz150069,f_150091,sz150091,f_150054,sz150054,f_150099,sz150099,f_150118,sz150118,f_150187,sz150187,f_160212,sz160212,f_150145,sz150145,f_150145,sz150145,f_150182,sz150182,f_150016,sz150016,f_161115,sz161115,f_150060,sz150060,f_150180,sz150180,f_150093,sz150093,f_150052,sz150052,f_161505,sz161505,f_150089,sz150089,f_150124,sz150124,f_150077,sz150077,f_150151,sz150151,f_160915,sz160915,f_150204,sz150204,f_150120,sz150120,f_150120,sz150120,f_150036,sz150036,f_150134,sz150134,f_150064,sz150064,f_150199,sz150199,f_150058,sz150058,f_150023,sz150023,f_150009,sz150009,f_150072,sz150072,f_150200,sz150200,f_150192,sz150192,f_150095,sz150095,f_150059,sz150059,f_150147,sz150147,f_150147,sz150147,f_150128,sz150128,f_150128,sz150128,f_150031,sz150031,f_150097,sz150097,f_150205,sz150205,f_150001,sz150001,f_150185,sz150185,f_150198,sz150198,f_150017,sz150017,f_150105,sz150105,f_150146,sz150146,f_150022,sz150022,f_150088,sz150088,f_150012,sz150012,f_150129,sz150129,f_150129,sz150129,f_150193,sz150193,f_150084,sz150084,f_150181,sz150181,f_150181,sz150181,f_150209,sz150209,f_150008,sz150008,f_150035,sz150035,f_150055,sz150055,f_150177,sz150177,f_150177,sz150177,f_150100,sz150100,f_150100,sz150100,f_150013,sz150013,f_150210,sz150210,f_162712,sz162712,f_150184,sz150184,f_150161,sz150161,f_150161,sz150161,f_150021,sz150021,f_164902,sz164902,f_150101,sz150101,f_150051,sz150051,f_150157,sz150157,f_150157,sz150157,f_150081,sz150081,f_150085,sz150085,f_164105,sz164105,f_150018,sz150018,f_150102,sz150102,f_150102,sz150102,f_161713,sz161713,f_161813,sz161813,f_150137,sz150137,f_150053,sz150053,f_150073,sz150073,f_160618,sz160618,f_150070,sz150070,f_161216,sz161216,f_150076,sz150076,f_150148,sz150148,f_150148,sz150148,f_150042,sz150042,f_150042,sz150042,f_161015,sz161015,f_150160,sz150160,f_150160,sz150160,f_150113,sz150113,f_150158,sz150158,f_150169,sz150169,f_150169,sz150169,f_160621,sz160621,f_150150,sz150150,f_150150,sz150150,f_164208,sz164208,f_150067,sz150067,f_150067,sz150067,f_150130,sz150130,f_150130,sz150130,f_150154,sz150154,f_150154,sz150154,f_150175,sz150175,f_150138,sz150138,f_150138,sz150138,f_150140,sz150140,f_150140,sz150140,f_150039,sz150039,f_166401,sz166401,f_150132,sz150132,f_150132,sz150132,f_161911,sz161911,f_150019,sz150019,f_150106,sz150106,f_150106,sz150106,f_163819,sz163819,f_150075,sz150075,f_160513,sz160513,f_161908,sz161908,f_150108,sz150108,f_150082,sz150082,f_150082,sz150082,f_150133,sz150133,f_150133,sz150133,f_150117,sz150117,f_150117,sz150117,f_150156,sz150156,f_150156,sz150156,f_150170,sz150170,f_150164,sz150164,f_150032,sz150032,f_164606,sz164606,f_150020,sz150020,f_161614,sz161614,f_150034,sz150034,f_150027,sz150027,f_150027,sz150027,f_150040,sz150040,f_150040,sz150040,f_166013,f_166012,f_000776,f_150096,sz150096,f_150096,sz150096,f_000909,f_165808,f_000910,f_000911,f_121007,f_121099,f_000091,f_150002,f_150104,sz150104,f_150003,f_150006,f_150007,f_165706,f_000093,f_165518,f_165517,f_000291,f_150010,f_164813,f_164704,f_150011,f_150114,sz150114,f_150114,sz150114,f_150115,sz150115,f_150115,sz150115,f_150116,f_150116,f_000292,f_000293,f_000293,f_150119,f_150119,f_000316,f_000317,f_164703,f_000318,f_000318,f_164510,f_164509,f_000340,f_150127,f_150127,f_000341,f_000092,f_000342,f_150025,f_150026,f_150026,f_164303,f_000342,f_000357,f_550016,f_000358,f_550015,f_150135,f_150136,f_000358,f_000382,f_000383,f_000384,f_000384,f_000387,f_150037,sz150037,f_150038,sz150038,f_150038,sz150038,f_164302,f_000388,f_000388,f_000428,f_150041,f_150041,f_000429,f_000430,f_150043,sz150043,f_164211,f_150043,sz150043,f_150044,sz150044,f_150045,sz150045,f_164210,f_164209,f_150045,sz150045,f_150046,sz150046,f_519059,f_519058,f_519058,f_000430,f_000453,f_000454,f_150159,f_150159,f_000455,f_000455,f_000497,f_150056,sz150056,f_150162,f_150162,f_519057,f_000498,f_000499,f_150166,f_150166,f_000499,f_150061,sz150061,f_150061,sz150061,f_164207,f_164206,f_150062,sz150062,f_150063,sz150063,f_150063,sz150063,f_000500,f_519055,f_519053,f_163910,f_163909,f_000501,f_000502,f_150068,sz150068,f_150068,sz150068,f_000502,f_000622,f_519053,f_000623,f_000624,f_150196,f_150197,f_000624,f_000631,f_000632,f_150078,sz150078,f_150203,sz150203,f_150078,sz150078,f_150079,f_150079,f_519052,f_167502,f_150211,f_150212,f_150213,f_150214,f_150215,f_150216,f_150217,f_150218,f_150223,f_150224,f_000633,f_163908,f_163826,f_163825,f_000633,f_160514,f_000674,f_150083,sz150083,f_160619,f_000674,f_160623,f_163006,f_163004,f_163003,f_000675,f_162512,f_162511,f_160811,f_167501,f_000675,f_166106,f_161016,f_162215,f_162109,f_162106,f_000676,f_162105,f_000676,f_166105,f_161506,f_166022,f_161626,f_161627,f_000774,f_161717,f_166021,f_161909,f_166017,f_161824,f_000775,f_161828,f_161827,f_550016,f_150048,sz150048,f_150149,sz150149,f_150071,sz150071,f_150030,sz150030,f_150098,sz150098,f_150121,sz150121,f_150121,sz150121,f_150107,sz150107,f_150143,sz150143,f_150066,sz150066,f_150123,sz150123,f_150123,sz150123,f_150094,sz150094,f_150094,sz150094,f_150179,sz150179,f_150179,sz150179,f_150176,sz150176,f_150086,sz150086,f_164808,sz164808,f_150152,sz150152,f_150152,sz150152,f_160617,sz160617,f_150131,sz150131,f_165509,sz165509,f_150153,sz150153,f_150090,sz150090,f_150090,sz150090,f_150028,sz150028,f_150047,sz150047,f_150092,sz150092,f_150092,sz150092,f_150112,sz150112,f_150112,sz150112,f_150057,sz150057,f_150110,sz150110,f_150110,sz150110,f_150109,sz150109,f_150065,sz150065,f_150171,sz150171,f_150171,sz150171,f_150049,sz150049,f_161207,sz161207,f_161026,sz161026,f_165519,sz165519,f_165520,sz165520,f_165521,sz165521,f_165705,sz165705,f_161024,sz161024,f_161022,sz161022,f_165809,sz165809,f_161014,sz161014,f_160806,sz160806,f_160630,sz160630,f_160629,sz160629,f_160628,sz160628,f_160626,sz160626,f_150087,sz150087,f_150087,sz150087,f_160625,sz160625,f_150080,sz150080,f_167601,sz167601,f_150080,sz150080,f_163113,sz163113,f_161826,sz161826,f_160222,sz160222,f_161825,sz161825,f_160221,sz160221,f_160219,sz160219,f_161720,sz161720,f_165311,sz165311,f_161718,sz161718,f_164705,sz164705"
    fund_list = fund_string.split(",")
    fund_data_list_code = []
    fund_stock_list_code = []
    for item in fund_list:
        if item[0] == 'f':
            fund_data_list_code.append(item)
        else:
            fund_stock_list_code.append(item)
    return (fund_data_list_code, fund_stock_list_code)

def get_creative_fund(code):
    loop_variable = True
    while(loop_variable):
        try:
            url = "http://hq.sinajs.cn/rn=ry1yo&list=" + code
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            raw_data = unicode(res.read(), "GB2312")
            raw_data = raw_data[21:-3] + "," + code[2:]
            raw_data = raw_data.split(",")
            loop_variable = False
        except:
            loop_variable = True
    # print "fund", len(raw_data)
    return raw_data

def get_creative_fund_stock(code):
    loop_variable = True
    while(loop_variable):
        try:
            url = "http://hq.sinajs.cn/rn=ry1yo&list=" + code
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            raw_data = unicode(res.read(), "GB2312")
            raw_data = code[2:] + "," + raw_data[21:-3]
            raw_data = raw_data.split(",")
            loop_variable = False
        except:
            loop_variable = True
    # print "stock", len(raw_data)
    return raw_data

def save_data(table_name):
    fund_data_list = []
    fund_stock_list = []
    if (table_name[-2:] == "FD"):
        fund_data_list_code = split_fund_stock()[0]
        for code in fund_data_list_code:
            fund_data = get_creative_fund(code)
            fund_data_list.append(fund_data)
        fund_data_df = pd.DataFrame(fund_data_list, columns=["F_name", "F_net", "F_Tnet", "B_D_net", "F_date_net", "F_Tamount", "code"])
        fund_data_df['get_date'] = get_date
        try:
            op_db.save(fund_data_df, table_name) #FD is fund
        except:
            fund_data_df.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, get_date))
    else:
        fund_stock_list_code = split_fund_stock()[1]
        for code in fund_stock_list_code:
            fund_data_stock = get_creative_fund_stock(code)
            fund_stock_list.append(fund_data_stock)
        fund_stock_df = pd.DataFrame(fund_stock_list)
        fund_stock_df = fund_stock_df[range(0, 9)] #+range(31, 33)]
        fund_stock_df.columns = ["code", "Name", "TOprice", "YCprice", "Cprice", "THprice", "TLprice", "DealData", "DealAmout"]#, "get_date", "Time"]
        fund_stock_df["get_date"] = get_date
        try:
            op_db.save(fund_stock_df, "fund_creative_SK") # SK is stock
        except:
            fund_stock_df.to_csv("/home/frank/stock/data/{0}_{1}.csv".format(table_name, get_date))

if __name__ == "__main__":
    save_data("fund_creative_FD")

    # print fund_list
    # fund_data_list_code = []
    # fund_stock_list_code = []
    # fund_data_list = []
    # fund_stock_list = []
    # for item in fund_list:
    #     if item[0] == 'f':
    #         fund_data_list_code.append(item)
    #     else:
    #         fund_stock_list_code.append(item)
    # for code in fund_data_list_code:
    #     fund_data = get_creative_fund(code)
    #     fund_data_list.append(fund_data)
    # fund_data_df = pd.DataFrame(fund_data_list, columns=["F_name", "F_net", "F_Tnet", "B_D_net", "F_date_net", "F_Tamount", "code"])
    # fund_data_df['get_date'] = strftime('%Y-%m-%d', gmtime())
    # op_db.save(fund_data_df, "fund_creative_FD") #FD is fund
    # for code in fund_stock_list_code:
    #     fund_data_stock = get_creative_fund_stock(code)
    #     fund_stock_list.append(fund_data_stock)
    # fund_stock_df = pd.DataFrame(fund_stock_list)
    # fund_stock_df = fund_stock_df[range(0, 9)+range(31, 33)]
    # fund_stock_df.columns = ["code", "Name", "TOprice", "YCprice", "Cprice", "THprice", "TLprice", "DealData",
    #                                  "DealAmout", "get_date", "Time"]
    # op_db.save(fund_stock_df, "fund_creative_SK") # SK is stock