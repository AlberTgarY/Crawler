from vector_unit import list_3_ngram
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import joblib
from sklearn.datasets import base
import _pickle as pickle



def TDM(bunch, temp_dat):
    temp = []
    idfBunch = base.Bunch(tdm=[])

    for content in bunch.contents:
        temp = temp + content
    train_tfidfbunch = read_dat("train_tfidf.dat")
    idfBunch.vocabulary = train_tfidfbunch.vocabulary
    vectorizer = CountVectorizer(vocabulary=train_tfidfbunch.vocabulary)  # count frequency
    transformer = TfidfTransformer()  # tf-tdf weight
    freq = vectorizer.fit_transform(temp)  # freq.toarray() frequency array
    tfidf = transformer.fit_transform(freq)  # tfidf.toarray() tfidf matrix
    idfBunch.tdm = tfidf

    with open("./dat/" + temp_dat, "wb") as file_obj:
        pickle.dump(idfBunch, file_obj)


def list_3_ngrams():
    test = ["原标题：不法商人“围猎”领导干部，“套路”背后是什么？　　半月谈评论员字强　　“我们就是猎人，领导就是猎物。”　　“"
            "在我们眼中，他就是我们获取利益的一个工具。”　　“他首先获取了你的信任，之后才跟你一步一步提出小事情的帮忙，再到大事情"
            "帮忙，之后再跟上重金贿赂，利益输送。”　　“不管他说得多甜言蜜语，喊你爹妈，喊你大爷，喊你恩人，你都不要当真，我就是当真"
            "了。”　　……　　近期，云南省纪委监委推出反腐警示专题片《围猎：行贿者说》，从“围猎”者和被“围猎”者双方角度，揭示了官商之"
            "间过从甚密、利益勾连、蝇营狗苟的乱象，不法商人与被“围猎”官员现身说法，声泪俱下地道出了“围猎”的"
            "本质和“大梦初醒”的悔恨心理，令人唏嘘，催人警醒。　　专题片中，不法商人程绪库在一次饭局上认识了云南省人大财政经济委员会",

            "周四指数红盘收，可市场情绪非常差，出逃资金明显。周五当低吸赚不到钱时候，大家都选择了一键清仓，指数也就崩了，这算不算人为干预的股灾呢？早上盘"
            "面的下砸基本把大部分人吓尿了，如果是做短线的基本又是少不了割肉。然后尾盘指数拉起来点，心态也彻底崩了。以前行情好的时候，当天是拉大金融，之后是"
            "拉科技股，大家一起赚钱high。今年下半年的行情是，没有增量资金，那么就先拉大金融，过些日子拉科技股。现在行情是局部科技股走牛，大金融歇菜。缺乏赚钱"
            "效应，或者你低吸当天吃肉，第二天直接砸盘，让你没利润。这种奇葩行情是不值得留念的。别看大盘指数跌得凄凄惨惨，短线接力的情绪其实是回暖的。周五没有出"
            "现核按钮的局面，高位票和低位票承接都非常不错，这种承接的强度其实是超预期的。创业板天山生物涨停，大家知道这是20cm的首个妖",

            "原标题：31省份11月CPI出炉：22地物价降了！海南降最猛　　中新经纬客户端12月12日电（董湘依）国家统计局11日公布31省份2020年11月居民消费"
            "价格指数（CPI），数据显示，22个省份11月CPI同比录得负增长，而海南为跌幅最大的省份，降幅达1.9%。仅8省份CPI同比上涨，西藏涨0.9%领涨全国。　"
            "　降降降！22省份物价负增长　　国家统计局日前公布的数据显示，11月全国CPI同比下降0.5%，为时隔11年后再现负增长。各地物价也纷纷骤降，海南、湖北"
            "、湖南、山东、河北等22个省份11月CPI同比录得负增长，其中海南CPI同比降1.9%，为全国降幅最大省份。　　17省份CPI涨幅数据超过了全国水平，其中，"
            "、青海、云南、甘肃、北京、新疆、山西、浙江这8个省份的CPI为正增长，西",

            "　　原标题：四川威远男子杀害失足女潜逃21年被抓 犯故意杀人罪被判12年　　21年前，四川威远男子罗某持匕首杀害一名失足女子，随后潜逃。直到今年6月，罗"
            "某被警方抓获归案。12月11日，中国裁判文书网公开了罗某犯故意杀人罪一案的判决书，他被判处有期徒刑12年。　　今年41岁的罗某系内江市威远人，住相邻的"
            "自贡市大安区，从事个体废品收购。据公诉机关指控，1999年3月23日下午，罗某从内江出发乘坐公共汽车到威远县城找朋友余某玩耍。到了后无法联系上余某，便"
            "入住县城的渔业招待所。当晚10时左右，罗某经招待所承包人介绍，与卖淫女曹某发生了卖淫嫖娼行为，之后曹某离开房间。又过了一段时间，被害人唐某经招待所"
            "承包人介绍，前往罗某所住房间从事卖淫活动，双方发生性关系后，因费用问题发生争执。　　公诉机关指控还称，"]
    Raw = base.Bunch(contents=[])
    for t in test:
        Raw.contents.append(list_3_ngram(t))
    return Raw

def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch

def create_dat(dat_name="for_test.dat"):
    Raw = list_3_ngrams()
    TDM(Raw, dat_name)

create_dat()
new_svm = joblib.load('./model/clf.pkl')
test_dat = read_dat("for_test.dat")
print(new_svm.predict(test_dat.tdm))