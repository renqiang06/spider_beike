## 爬取贝壳网部分地区的房源信息


1. 指定城市、地区
```
city = 'sh'
dict_districts = {'pd': ['nanmatou'], 'jd': ['waigang', 'anting']}
```
2. 获取基本信息
    ``` 
    [
        'time', 'city', 'region', 'district', 'address', 'housedel_id', 'floor', 'totalFloor',
        'year', 'area', 'roomType', 'direction', 'totalPrice', 'meterPrice',
        'followers', 'publishDate', 'maidianDetail', 'goodhouse_tag', 'href', 'dataAction'
        ]
    ```

3. 数据存储到excel
```
spider_beike.xlsx
```

