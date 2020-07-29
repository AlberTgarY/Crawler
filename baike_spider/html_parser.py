# coding=utf-8

import re
from urllib import parse
from bs4 import BeautifulSoup

# HTML 解析器
import html_downloader


def get_content(news_content):
    # get the news info and  make it a string
    temp = ''
    for new in news_content:
        temp = temp + new.get_text().replace('\n','')
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
        count = 20
        # 查找页面的 URL
        links = soup.find_all('a')
        for link in links:
            count = count - 1
            if (count >= 0):
                new_url = link['href']
                # 将 new_url 按照 page_url 的格式拼接
                print(new_url)
                new_url_join = parse.urljoin(page_url, new_url)
                new_urls.add(new_url_join)
        return new_urls

    # 获取页面中想要的 DATA
    def _get_new_data(self, page_url, soup):

        self.downloader = html_downloader.HtmlDownloader()
        res_data = {'url': page_url}
        count = 100
        # contain all news in current page
        res_urls = {}
        res_news = {}
        # search for news link
        summary_node = soup.find_all(href=re.compile(r'http(s?)(://)'))
        for n in summary_node:
            count = count - 1
            if(count>=0):
                html_cont = self.downloader.download(n['href'])
                soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
                try:
                    # search for content
                    news_content = soup.find_all('p')
                    temp = get_content(news_content)
                    print(temp[0:300])
                    title = n.get_text().replace('\n', '')
                    res_news[title] = temp[0:300]
                    res_urls[title] = n['href']
                    print("Find news in site: " + n['href'])
                except ValueError as e:
                    print(e)
                except:
                    print("Cant find news in this site")
                finally:
                    res_data['summary'] = res_news
                    res_data['website'] = res_urls
                    print("res_news size : " + str(len(res_data['summary'])))
        return res_data

    # 解析网页获取 new_urls 与 new_data
    def parse(self, page_url, html_cont):

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data
