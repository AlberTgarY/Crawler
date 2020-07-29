# coding=utf-8
import ssl
import os
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
            r = request.Request(url=url,headers=headers)
            response = request.urlopen(r, context=context)
            if response.getcode() != 200:
                return None
            else:
                return response.read()
        except Exception as e:
            print(url+' got a error: [' + str(e) +"]")
            if str(e) == 'HTTP Error 404: Not Found':
                file_name = "404.txt"
                with open(file_name, 'a') as object:
                    object.write(url+"\n")
                    print(url+" has been recorded")
            return None



