## 爬取贝壳网部分地区的二手房源信息

* 指定城市、地区

```
city = 'sh'
dict_districts = {'pd': ['nanmatou'], 'jd': ['waigang', 'anting']}
```

* 获取房源基本信息

  ```python
  ['time', 'city', 'region', 'district', 'address', 'housedel_id', 'floor', 'totalFloor',
  'year', 'area', 'roomType', 'direction', 'totalPrice', 'meterPrice',
  'followers', 'publishDate', 'maidianDetail', 'goodhouse_tag', 'href', 'dataAction']
  ```
* 数据存储到excel

```
spider_beike.xlsx
```

* 发送邮件
  ```

  msg_from = '**qq.com'  # 发送方邮箱地址。
  password = '**'  # 发送方QQ邮箱授权码，不是QQ邮箱密码。
  msg_to = '**@126.com'  # 收件人邮箱地址。

  subject = "你好"  # 主题。
  content = "i am **"  # 邮件正文内容。
  msg = MIMEText(content, 'plain', 'utf-8')

  msg['Subject'] = subject
  msg['From'] = msg_from
  msg['To'] = msg_to

  try:
      client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
      print("连接到邮件服务器成功")

      client.login(msg_from, password)
      print("登录成功")

      client.sendmail(msg_from, msg_to, msg.as_string())
      print("发送成功")
  except smtplib.SMTPException as e:
      print("发送邮件异常")
  finally:
      client.quit()
  ```
