#!/usr/bin/python
# -*- coding: utf-8 -*-
import op_database as op_db
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

temp_data = op_db.read("select * from test.fund_creative_rate")
temp_data['get_date'] = pd.to_datetime(temp_data.get_date, format='%Y-%m-%d')
# print temp_data


plt.plot(temp_data.get_date, temp_data.rate, '.')
plt.text(temp_data.get_date, temp_data.rate, '0')
# matplotlib.axes.Axes.text(temp_data.get_date, temp_data.rate, temp_data.code)

plt.show()
