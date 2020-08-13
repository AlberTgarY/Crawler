# s = '国'
#
# b = 'Ô­±êÌâ£ºÊ®Èý½ìÈ«¹úÈË´óÈý´Î»áÒéÔÚ¾©±ÕÄ»£©'
# e = bytes(b , encoding='GBK')
# c = b.decode('GBK')
# print(c)
# from fake_useragent import UserAgent
# ua = UserAgent()
#
# #最常用的方式
# #写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
# print(ua.random)
import configparser
#        https://news.163.com/
#        http://news.baidu.com/
# 读取配置文件
config = configparser.RawConfigParser()
config.read("cfg.ini")

# 获取文件的所有section
# secs = config.sections()
# print(secs)

# 获取指定section下的所有参数key
# options = config.options("test1")
# print(options)

# 获取指定section中指定key的value
# http://www.people.com.cn/
# http://www.xinhuanet.com/
# https://www.ifeng.com/
# https://news.sina.com.cn/

# from datetime import datetime
# import os
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#
# if __name__ == '__main__':
#     scheduler = BlockingScheduler()
#     scheduler.add_job(tick, 'interval', seconds=3)
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
#
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass
import openpyxl
import pandas as pd

wb = openpyxl.load_workbook('测试.xlsx')
#如果有多个模块可以读写excel文件，这里要指定engine，否则可能会报错
writer = pd.ExcelWriter('测试.xlsx', engine='openpyxl')
#没有下面这个语句的话excel表将完全被覆盖
writer.book = wb

df = pd.DataFrame(pd.read_excel('测试.xlsx', sheet_name = 'Sheet1'))
#如果有相同名字的工作表，新添加的将命名为Sheet21，如果Sheet21也有了就命名为Sheet22，不会覆盖原来的工作表
df.to_excel(writer,sheet_name = 'Sheet2',index = None)
writer.save()
writer.close()