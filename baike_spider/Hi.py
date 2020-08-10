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

# 读取配置文件
config = configparser.RawConfigParser()
config.read("cfg.ini")

# 获取文件的所有section
secs = config.sections()
print(secs)

# 获取指定section下的所有参数key
# options = config.options("test1")
# print(options)

# 获取指定section中指定key的value
param = config.get("crawler", "craw_root_num")
print(param)
