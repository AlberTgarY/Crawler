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
import os
#        https://news.163.com/
#        http://news.baidu.com/
# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")

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

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging

logging.basicConfig(level=logging.INFO,
format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
datefmt = '%Y-%m-%d %H:%M:%S',
filename = 'log1.txt',
filemode = 'a')


def aps_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


def date_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    print(1 / 0)


def my_listener(event):
    if event.exception:
        print('任务出错了！！！！！！')

    else:
        print('任务照常运行...')

scheduler = BlockingScheduler()

scheduler.add_job(func=date_test, args=('一次性任务,会出错',),
                  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=15), id='date_task')

scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3, id='interval_task')

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler._logger = logging

scheduler.start()
