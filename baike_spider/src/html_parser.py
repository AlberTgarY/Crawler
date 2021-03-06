# coding=utf-8

import re
import chardet
from urllib import parse
from bs4 import BeautifulSoup
# HTML 解析器
import html_downloader
import configparser
from Logger import get_log

# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")
logger = get_log()


def compare(url, file_name):
    for line in open(file_name):
        if line.strip('\n') == url:
            return True
    return False


def get_content(news_content):
    # get the news info and  make it a string
    temp = ''
    for new in news_content:
        temp = temp + new.get_text().replace('\n', '')
    if temp != '':
        return temp
    raise ValueError('content is None')


class HtmlParser(object):

    # Find the all indexes at the first search
    @staticmethod
    def _get_all_index(page_url, soup):

        new_urls = set()
        # 查找页面的 URL
        links = soup.find('div', class_="main-nav").find_all('a')
        for link in links:
            new_url = link['href']
            # 将 new_url 按照 page_url 的格式拼接
            new_url_join = parse.urljoin(page_url, new_url)
            new_urls.add(new_url_join)
            logger.debug("New added index url: "+ new_url_join)
        return new_urls

    # 获取页面中所有的 URL
    @staticmethod
    def _get_new_urls(page_url, soup):

        new_urls = set()
        count = int(config.get("crawler", "craw_url_num"))
        # 查找页面的 URL
        try:
            links = soup.find_all('a')
            for link in links:
                count = count - 1
                if count >= 0:
                    new_url = link['href']
                    # 将 new_url 按照 page_url 的格式拼接
                    # print(new_url)
                    new_url_join = parse.urljoin(page_url, new_url)
                    new_urls.add(new_url_join)
                    logger.debug("New added url: " + new_url_join)
        except Exception as e:
            print(e)

        return new_urls

    # 获取页面中想要的 DATA
    def _get_new_data(self, page_url, soup):

        INVALID_URL_TXT_PATH = str(config.get("path", "txt_path"))
        # download html
        self.downloader = html_downloader.HtmlDownloader()
        res_data = {'url': page_url}
        count = int(config.get("crawler", "craw_data_num"))
        # contain all news in current page
        res_urls = {}
        res_news = {}
        # search for news link
        summary_node = soup.find_all(href=re.compile(r'htm'))
        #print(summary_node)
        if summary_node != []:
            for n in summary_node:
                count = count - 1
                if count >= 0:
                    result = compare(n['href'], INVALID_URL_TXT_PATH)
                    if not result:
                        # start crawling
                        logger.info("Start downloading url: " + n['href'])
                        html_cont = self.downloader.download(n['href'])

                        if html_cont == None:
                            logger.info("This url is NoneType, crawling skipped.")
                            print("This urls` html has NoneType Error, continue crawling")
                            continue
                        encoded_type = chardet.detect(html_cont)['encoding']
                        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding=str(encoded_type))
                        try:
                            # search for content
                            print("Try to search: " + n['href'])
                            print("Encoded type: " + encoded_type)
                            news_content = soup.find_all('p')
                            temp = get_content(news_content)
                            length = int(config.get("crawler", "craw_data_length"))
                            print(temp[0:length])
                            logger.debug("Found content : " + temp[0:30] + "...")
                            # brief description
                            title = n.get_text().replace('\n', '')
                            res_news[title] = temp[0:length]
                            res_urls[title] = n['href']
                        except ValueError as e:
                            logger.debug("Got a ValueError: " + str(e))
                            print(e)
                        except Exception as e:
                            print(e)
                        finally:
                            res_data['summary'] = res_news
                            res_data['website'] = res_urls
                            print("res_news size : " + str(len(res_data['summary'])))
                    else:
                        logger.info(n['href'] + " has HTTP ERROR")
                        # find the website in the history
                        res_news[n['href']] = "HTTP ERROR"
                        res_urls[n['href']] = n['href']
                        res_data['summary'] = res_news
                        res_data['website'] = res_urls
                        print("This url is invalid: " + n['href'])
                        # print("res_news size : " + str(len(res_data['summary'])))
                        continue
        else:
            logger.info("root url: "+ page_url + " has NO CONTENT")
            res_news[page_url] = "NO CONTENT"
            res_urls[page_url] = page_url
            res_data['summary'] = res_news
            res_data['website'] = res_urls
        return res_data

    # 解析网页获取 new_urls 与 new_data
    def parse(self, page_url, html_cont, encoded_type):
        logger.info("Start parsing")
        if page_url is None or html_cont is None:
            logger.debug("Can`t find anything!")
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding=str(encoded_type))

        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data
