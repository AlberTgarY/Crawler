import re
import jieba
import configparser

# 读取配置文件
config = configparser.RawConfigParser()
config.read("../temp/cfg.ini")


class stopword(object):

    def Chinese_Stopwords(self):
        stop_word = []
        cfp = open(config.get("path", "stopwords_path"),encoding='utf-8')
        for line in cfp:
            for word in line.split():
                stop_word.append(word)
        cfp.close()
        return stop_word

    def Word_cut_list(self, word_str):
        # keep the letter, num and chinese words
        word_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", '', word_str)
        # jieba cut
        word_list = list(jieba.cut(word_str))
        word_list_N = []
        chinese_stopwords = self.Chinese_Stopwords()
        # get rid of the stopwords
        for word in word_list:
            if word not in chinese_stopwords:
                word_list_N.append(word)
        return word_list_N
