# s = '国'

b = '£¨Ô­±êÌâ£º Ï°½üÆ½Ðû²¼±±¶·ÈýºÅÈ«ÇòÎÀÐÇµ¼º½ÏµÍ³ÕýÊ½¿ªÍ¨£©'
e = bytes(b , encoding='gbk')
c = e.decode('gbk')
print(c)
# from fake_useragent import UserAgent
# ua = UserAgent()
#
# #最常用的方式
# #写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
# print(ua.random)
