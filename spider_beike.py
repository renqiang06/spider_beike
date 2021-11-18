#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ren Qiang'
# %% 爬取贝壳数据


import requests
from lxml import etree
import json
import time
import re
import random
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', }

try:
    result = pd.read_excel("./beike.xlsx", sheet_name=0,
                           index_col=0)  # 读取excel数据文件
except:
    result = pd.DataFrame(columns=[
        'time', 'city', 'region', 'district', 'address', 'housedel_id', 'floor', 'totalFloor',
        'year', 'area', 'roomType', 'direction', 'totalPrice', 'meterPrice',
        'followers', 'publishDate', 'maidianDetail', 'goodhouse_tag', 'href', 'dataAction'])


city = 'sh'
dict_districts = {'pd': ['nanmatou'], 'jd': ['waigang', 'anting']}
regions = list(dict_districts.keys())
for region in regions:
    for district in dict_districts[region]:
        print(district)
        url_getPageNum = 'https://{0}.ke.com/ershoufang/{1}'.format(
            city, district)

        resp = requests.get(url=url_getPageNum, headers=headers).text
        _element = etree.HTML(resp)
        page = json.loads(_element.xpath(
            '//div[@class="page-box house-lst-page-box"]/@page-data')[0])["totalPage"]
        print(page)
        for i in range(page):
            url = '{0}/pg{1}/'.format(url_getPageNum, i+1)
            print(url)
            resp = requests.get(url=url, headers=headers).text
            _element = etree.HTML(resp)
            tags = _element.xpath('//li/div[@class="info clear"]')
            for tag in tags:
                temp = {}
                # 房源卖点及小区
                temp['maidianDetail'] = tag.xpath('./div[1]/a/text()')[0]
                temp['href'] = tag.xpath('./div[1]/a/@href')[0]
                temp['dataAction'] = tag.xpath('./div[1]/a/@data-action')[0]
                _dataActions = temp['dataAction'].split("&")
                for _aa in _dataActions:
                    if 'housedel_id' in _aa:
                        temp['housedel_id'] = _aa.split('=')[1]
                try:
                    temp['goodhouse_tag'] = tag.xpath(
                        './div[1]/span/text()')[0]
                except:
                    temp['goodhouse_tag'] = ''
                temp['address'] = tag.xpath('./div[2]/div[1]/div/a/text()')[0]
                # 房源基本情况：楼层、年份、面积、房型、朝向
                _houseInfo = tag.xpath('./div/div[@class="houseInfo"]/text()')
                _houseInfo = _houseInfo[1].replace(' ', '').split('\n')
                for j in _houseInfo:
                    if '' in _houseInfo:
                        _houseInfo.remove('')
                _floor = _houseInfo[0]
                temp['floor'] = _floor
                _totalFloor = int(re.search("共(.*?)层", (_houseInfo[1])).group(1))
                temp['totalFloor'] = _totalFloor
                if len(_houseInfo) == 5:
                    year = int(re.search("\|(.*?)年建\|",
                                         (_houseInfo[2])).group(1))
                else:
                    year = ''
                temp['year'] = year
                _area = float(re.search("\|(.*?)平米", (_houseInfo[-2])).group(1))
                temp['area'] = _area
                _roomType = re.search("(.*?)\|", (_houseInfo[-2])).group(1)
                temp['roomType'] = _roomType
                _direction = _houseInfo[-1].replace('|', '')
                temp['direction'] = _direction

                # 房源关注情况
                _followInfo = tag.xpath('./div/div[@class="followInfo"]/text()')
                for k in range(len(_followInfo)):
                    _followInfo[k] = _followInfo[k].replace(
                        '\n', '').replace('\r', '').replace(' ', '')

                _followers = int(
                    re.search("(.*?)人关注", (_followInfo[1])).group(1))
                temp['followers'] = _followers
                _publishDate = re.search("/(.*?)前发布", (_followInfo[1])).group(1)
                temp['publishDate'] = _publishDate

                # 房源tag
                subway = tag.xpath('./div/div/span[@class="subway"]/text()')

                # 房源价价格、单价
                _totalPrice = float(
                    tag.xpath('./div[2]/div[5]/div[1]/span/text()')[0].replace(' ', ''))
                _meterPrice = tag.xpath('./div[2]/div[5]/div[2]/span/text()')[0]
                _meterPrice = float(
                    re.search("(.*?)元/平", _meterPrice).group(1).replace(',', ''))
                temp['totalPrice'] = _totalPrice
                temp['meterPrice'] = _meterPrice
                temp['city'] = city
                temp['region'] = region
                temp['district'] = district
                temp['time'] = time.strftime("%Y%m%d-%H%M%S", time.localtime())
                result = result.append(temp, ignore_index=True)

            time.sleep(random.randint(0, 16))
result.to_excel(excel_writer='spider_beike.xlsx', sheet_name='beike')
# print(result, len(result))