# coding=utf-8
import os
import chardet
import url_manager, html_downloader, html_parser, html_outputer
import configparser
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# 读取配置文件
config = configparser.RawConfigParser()
config.read("cfg.ini")

def compare(url, file_name):
    for line in open(file_name):
        if line.strip('\n') == url:
            return True
    return False

def create_file404():
    if os.path.exists('404.txt'):
        return None
    else:
        f = open('404.txt', 'w+')
        f.seek(0)
        f.close()


# 爬虫主调程序，主要逻辑
class SpiderMain(object):

    # 初始化，设置 URL 管理器、下载器、解析器、输出器
    def __init__(self):

        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):

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
                result = compare(new_url, '404.txt')
                # time.sleep(random.random()*3)
                if not result:
                    html_cont = self.downloader.download(new_url)
                    encoded_type = chardet.detect(html_cont)['encoding']
                    new_urls, new_data = self.parser.parse(new_url, html_cont, encoded_type)
                    self.urls.add_new_urls(new_urls)
                    self.outputer.collect_data(new_data)

                    if count == int(config.get("crawler", "craw_root_num")):
                        break

                    count = count + 1
                else:
                    print("This url is invalid: " + new_url + " Try to craw another root url")
                    continue


            except Exception as e:
                print(e)

        self.outputer.output_excel()


if __name__ == "__main__":
    # 设置入口页 URL
    # https://news.sina.com.cn/  https://news.163.com/ http://news.baidu.com/
    create_file404()
    root_url = "http://www.people.com.cn/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
