# coding=utf-8
import ssl
import configparser
from urllib import request
from fake_useragent import UserAgent
from Logger import get_log

# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")
INVALID_URL_TXT_PATH = str(config.get("path", "txt_path"))

class HtmlDownloader(object):

    #   下载当前页，返回下载信息
    def download(self, url):
        logger = get_log()
        context = ssl._create_unverified_context()
        if url is None:
            raise ValueError('target url is None')
        if url[0:2] == '//' and url[2:5] == 'www':
            url = "http:"+url

        try:
            ua = UserAgent()
            # fake headers
            headers = {"User-Agent": ua.random}
            # request website
            r = request.Request(url=url, headers=headers)
            # r1 = requests.get(url=url, headers=headers, timeout=15)
            logger.info("urlopen: " + url)
            response = request.urlopen(r, context=context, timeout=15)

            # print(str(response.info()["Content-Type"]))
            if response.getcode() != 200:
                logger.info("url code: " + response.getcode())
                return None
            elif str(response.info()["Content-Type"]).find("text/html") == -1:
                if str(response.info()["Content-Type"]).find("text/xml") != -1:
                    logger.info("Read data successfully")
                    return response.read()
                raise Exception("The url type is not HTML")
            else:
                logger.info("Read data successfully")
                return response.read()
        except Exception as e:
            logger.info("Got a error while downloading: " + str(e))
            print(url+' got a error: [' + str(e) + "]")
            # if str(e) == 'HTTP Error 404: Not Found' or str(e) == 'The url type is not HTML':
            with open(INVALID_URL_TXT_PATH, 'a') as object:
                object.write(url+"\n")
                logger.info(url + "has been recorded")
                print(url+" has been recorded")
                return None




