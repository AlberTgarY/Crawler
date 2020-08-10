# coding=utf-8

import re
import chardet
from urllib import parse
from bs4 import BeautifulSoup
# HTML 解析器
import html_downloader
import configparser

# 读取配置文件
config = configparser.RawConfigParser()
config.read("cfg.ini")


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
    def _get_all_index(self, page_url, soup):

        new_urls = set()
        # 查找页面的 URL
        links = soup.find('div', class_="main-nav").find_all('a')
        for link in links:
            new_url = link['href']
            # 将 new_url 按照 page_url 的格式拼接
            new_url_join = parse.urljoin(page_url, new_url)
            new_urls.add(new_url_join)
        return new_urls

    # 获取页面中所有的 URL
    def _get_new_urls(self, page_url, soup):

        new_urls = set()
        count = int(config.get("crawler", "craw_url_num"))
        # 查找页面的 URL
        links = soup.find_all('a')
        for link in links:
            count = count - 1
            if (count >= 0):
                new_url = link['href']
                # 将 new_url 按照 page_url 的格式拼接
                # print(new_url)
                new_url_join = parse.urljoin(page_url, new_url)
                new_urls.add(new_url_join)
        return new_urls

    # 获取页面中想要的 DATA
    def _get_new_data(self, page_url, soup):

        self.downloader = html_downloader.HtmlDownloader()
        res_data = {'url': page_url}
        count = int(config.get("crawler", "craw_data_num"))
        # contain all news in current page
        res_urls = {}
        res_news = {}
        # search for news link
        summary_node = soup.find_all(href=re.compile(r'html'))
        for n in summary_node:
            count = count - 1
            if (count >= 0):
                result = compare(n['href'], '404.txt')
                if not result:
                    # start crawling
                    html_cont = self.downloader.download(n['href'])
                    encoded_type = chardet.detect(html_cont)['encoding']
                    print("type: "+ encoded_type)
                    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding=str(encoded_type))
                    try:
                        # search for content
                        print("Try to search: " + n['href'])
                        news_content = soup.find_all('p')
                        temp = get_content(news_content)
                        print(temp[0:300])
                        # brief description
                        title = n.get_text().replace('\n', '')
                        res_news[title] = temp[0:300]
                        res_urls[title] = n['href']
                    except ValueError as e:
                        print(e)
                    except:
                        print("Cant find news in this site")
                    finally:
                        res_data['summary'] = res_news
                        res_data['website'] = res_urls
                        print("res_news size : " + str(len(res_data['summary'])))
                else:
                    # find the website in the history
                    res_news[n['href']] = "HTTP ERROR"
                    res_urls[n['href']] = n['href']
                    res_data['summary'] = res_news
                    res_data['website'] = res_urls
                    print("This url is invalid: " + n['href'])
                    # print("res_news size : " + str(len(res_data['summary'])))
                    continue
        return res_data

    # 解析网页获取 new_urls 与 new_data
    def parse(self, page_url, html_cont, encoded_type):

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding=str(encoded_type))

        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data
