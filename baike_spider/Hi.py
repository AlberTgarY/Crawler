# s = '国'
#
# s2 = s.encode('utf-8')
# for n in range(1, 5):
#     print(n)
# b = 'ÈË²ÎÓëÌÖÂÛÀ´Ô´ >  ÍøÒ×Êý¶ÁÓÖµ½ÁË¸ßÈý±ÏÒµÉúÐÄÇé×îìþìýµÄÊ±ºòÁË£¬´Ó2020Äê7ÔÂ23ÈÕ¿ªÊ¼£¬Â½'
# e = bytes(b,encoding='utf-8')
# c = e.decode('utf-8')
# print(c)
from fake_useragent import UserAgent
ua = UserAgent()

#最常用的方式
#写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
print(ua.random)
