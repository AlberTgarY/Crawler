# coding=utf-8

import re
import chardet
from urllib import parse
from bs4 import BeautifulSoup
# HTML 解析器
import html_downloader
import configparser
from Logger import get_log
from stopwords import stopword
import jieba

# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")
logger = get_log()
predict = {
    "体育": ["体育", "足球", "运动", "赛跑", "NBA", "比赛", "胜利", "领先", "赛季", "球队", "开局", "巨星",
           "球星", "退役", "连胜", "失败", "输", "绝杀", "篮球", "奥运会", "mvp", "进球", "国家队", "跳水"
            , "国家队", "比赛", "得分", "运动员", "VS", "罚下", "禁区", "突破", "裁判", "射门", "联赛"],
    "时政": ["时政", "紧急", "大陆", "部长", "外交", "关系", "时候", "局势", "挑战", "世界", "问题", "总统", "当地", "经济", "军队"
            , "基地", "发言人", "省长", "晋升", "职务", "会议", "人大", "书记", "组织", "威胁", "环球", "沟通", "谈判", "局长"
            , "部长", "科长", "政策", "省份", "国家队", "调查", "实地", "走访", "政治", "贸易", "政府", "主任", "市长", "外交"
            , "媒体", "国务卿", "两岸", "台湾", "香港"],
    "军事": [ "演习", "军事", "军舰", "士兵", "交火", "武装", "战地", "战场", "导弹", "潜艇", "航母", "战斗机", "轰炸机", "坦克"
            , "南海", "海军", "陆军", "空军", "火箭", "调查", "发射", "技术", "武器", "调查", "无人机", "喷气", "战机", "战舰"
            , "坠毁", "摧毁", "先进", "国防", "军队", "舰队", "解放军", "将军", "开战", "侦察机", "上空"]

}




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


def predict_type(news_content):
    Type = "未知"
    stopwords = stopword()
    words_list = stopwords.Word_cut_list(news_content)
    frequency_dict = {"体育": 0, "时政": 0, "军事": 0}
    for word in words_list:
        for TYPE, keyword_list in zip(predict.keys(), predict.values()):
            if word in keyword_list:
                frequency_dict[TYPE] = frequency_dict[TYPE]+1
    print(frequency_dict)
    temp_type = max(frequency_dict, key=frequency_dict.get)
    if(frequency_dict[temp_type] == 0):
        return Type
    else:
        Type = temp_type
        return Type

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
            logger.debug("New added index url: "+ new_url_join)
        return new_urls

    # 获取页面中所有的 URL
    def _get_new_urls(self, page_url, soup):

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
        res_type = {}
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
                            print(temp[0:300])
                            logger.debug("Found content : " + temp[0:30] + "...")
                            # brief description
                            title = n.get_text().replace('\n', '')
                            res_news[title] = temp[0:300]
                            res_urls[title] = n['href']
                            res_type[title] = predict_type(temp[0:300])
                        except ValueError as e:
                            logger.debug("Got a ValueError: " + str(e))
                            print(e)
                        except Exception as e:
                            print(e)
                        finally:
                            res_data['summary'] = res_news
                            res_data['website'] = res_urls
                            res_data['type'] = res_type
                            print("res_news size : " + str(len(res_data['summary'])))
                    else:
                        logger.info(n['href'] + " has HTTP ERROR")
                        # find the website in the history
                        res_news[n['href']] = "HTTP ERROR"
                        res_urls[n['href']] = n['href']
                        res_type[n['href']] = "NONE"
                        res_data['summary'] = res_news
                        res_data['website'] = res_urls
                        res_data['type'] = res_type
                        print("This url is invalid: " + n['href'])
                        # print("res_news size : " + str(len(res_data['summary'])))
                        continue
        else:
            logger.info("root url: "+ page_url + " has NO CONTENT")
            res_news[page_url] = "NO CONTENT"
            res_urls[page_url] = page_url
            res_type[page_url] = "NONE"
            res_data['summary'] = res_news
            res_data['website'] = res_urls
            res_data['type'] = res_type
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
