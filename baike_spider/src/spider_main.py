# coding=utf-8
import configparser
import os
import chardet
import html_downloader
import html_outputer
import html_parser
import url_manager
from Logger import get_log

# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")
logger = get_log()


def compare(url, file_name):
    logger.info("Start comparing ROOT URL: " + url)
    for line in open(file_name):
        if line.strip('\n') == url:
            return True
    return False


def create_file404():
    try:
        INVALID_URL_TXT_PATH = str(config.get("path", "txt_path"))
        if os.path.exists(INVALID_URL_TXT_PATH):
            logger.info("404.txt exist, located in " + INVALID_URL_TXT_PATH)
            return None
        else:
            f = open(INVALID_URL_TXT_PATH, 'w+')
            f.seek(0)
            f.close()
            logger.info("404.txt created.")
    except Exception as e:
        logger.debug(e)
        print(e)


# start crawling
def Start(root_url):
    logger.info("Crawler has started working. root url: " + "*** " + root_url + " ***")
    create_file404()
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)


# 爬虫主调程序，主要逻辑
class SpiderMain(object):

    # 初始化，设置 URL 管理器、下载器、解析器、输出器
    def __init__(self):

        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):

        path = str(config.get("path", "txt_path"))
        # 下载成功页面计数
        count = 0

        # 添加第一个 URL
        self.urls.add_new_url(root_url)

        # URL 管理器中存在 URL 时处理
        while self.urls.has_new_url():
            # print(self.urls.size())
            try:
                new_url = self.urls.get_new_url()

                print("craw %d : %s" % (count, new_url))
                result = compare(new_url, path)
                # time.sleep(random.random()*3)
                if not result:
                    logger.info("Start downloading current HTML: " + new_url)
                    html_cont = self.downloader.download(new_url)
                    encoded_type = chardet.detect(html_cont)['encoding']
                    new_urls, new_data = self.parser.parse(new_url, html_cont, encoded_type)
                    self.urls.add_new_urls(new_urls)
                    self.outputer.collect_data(new_data)

                    if count == int(config.get("crawler", "craw_root_num")):
                        logger.info("Crawling finished")
                        break

                    count = count + 1
                else:
                    print("This url is invalid: " + new_url + " Try to craw another root url")
                    continue


            except Exception as e:
                print(e)

        self.outputer.output_excel()

