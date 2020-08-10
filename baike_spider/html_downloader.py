# coding=utf-8
import ssl
import requests
from urllib import request
from fake_useragent import UserAgent
# HTML 下载器



class HtmlDownloader(object):


    #   下载当前页，返回下载信息
    def download(self, url):
        context = ssl._create_unverified_context()
        if url is None:
            raise ValueError('target url is None')

        try:
            ua = UserAgent()
            # fake headers
            headers = {"User-Agent": ua.random}
            # request website
            r = request.Request(url=url, headers=headers)
            # r1 = requests.get(url=url, headers=headers, timeout=15)
            response = request.urlopen(r, context=context, timeout=15)

            # print(str(response.info()["Content-Type"]))
            if response.getcode() != 200:
                return None
            elif str(response.info()["Content-Type"]).find("text/html") == -1:
                if str(response.info()["Content-Type"]).find("text/xml") != -1:
                    return response.read()
                raise Exception("The url type is not HTML")
            else:
                return response.read()
        except Exception as e:
            print(url+' got a error: [' + str(e) +"]")
            # if str(e) == 'HTTP Error 404: Not Found' or str(e) == 'The url type is not HTML':
            file_name = "404.txt"
            with open(file_name, 'a') as object:
                object.write(url+"\n")
                print(url+" has been recorded")
                return None




