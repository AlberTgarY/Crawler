import pandas as pd
import re
import string
import jieba

class stopword(object):


    def Chinese_Stopwords(self):          #导入停用词库
        stopword=[]
        cfp  = open('./model/cnews/hit_stopwords.txt',encoding='utf-8')   #停用词的txt文件
        for line in cfp:
            for word in line.split():
                stopword.append(word)
        cfp.close()
        return stopword


    def Word_cut_list(self, word_str):
        # 利用正则表达式去掉一些一些标点符号之类的符号。
        word_str = re.sub(r'\s+', ' ', word_str)  # trans 多空格 to空格
        word_str = re.sub(r'\n+', ' ', word_str)  # trans 换行 to空格
        word_str = re.sub(r'\t+', ' ', word_str)  # trans Tab to空格
        word_str = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+". \
                          encode("utf8").decode("utf8"), "".encode("utf8").decode("utf8"), word_str)
        wordlist = list(jieba.cut(word_str))  # jieba.cut  把字符串切割成词并添加至一个列表
        wordlist_N = []
        chinese_stopwords = self.Chinese_Stopwords()
        for word in wordlist:
            if word not in chinese_stopwords:  # 词语的清洗：去停用词
                if word != '\r\n' and word != ' ' and word != '\u3000'.encode("utf8").decode('unicode_escape') \
                        and word != '\xa0'.encode("utf8").decode('unicode_escape'):  # 词语的清洗：去全角空格
                    wordlist_N.append(word)
        return wordlist_N