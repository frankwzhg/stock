#!/user/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2

r = urllib2.urlopen("http://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqcxs").read()

soup = BeautifulSoup(r)
print soup
# fund_table = soup.find_all("tr", class_="selected")
# print fund_table