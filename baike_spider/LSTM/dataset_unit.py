from vector_unit import tf_idf,list_3_ngram,Embed
from sklearn.datasets import base
import _pickle as pickle


categories = ['体育','娱乐','家居','房产','教育',
       '时尚', '时政', '游戏', '科技', '财经']

categories_dict = {'体育':0,'娱乐':0,'家居':0,'房产':0,'教育':0,
       '时尚':0,'时政':0,'游戏':0,'科技':0,'财经':0}

files = {"train": "cnews.train.txt", "test": "cnews.test.txt", "val": "cnews.val.txt"}
dat = {"train": "cnews.train.dat", "test": "cnews.test.dat", "val": "cnews.val.dat"}


def parse_val(temp="cnews.vocab.txt"):
    with open("./data/"+temp, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    Bunch = base.Bunch(vocab=[])
    for line in lines:
        Bunch.vocab.append(line)
    with open("./dat/"+"cnews.vocab.dat", "wb") as file_obj:
        pickle.dump(Bunch, file_obj)


def parse_dataset(temp,num):

    with open("./data/"+temp, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    Bunch = base.Bunch(cat=[], contents=[])
    for line in lines:
        cat = line[0:2]
        content = line[3:103]
        if categories_dict[cat]<=num:
            gram_3 = list_3_ngram(content)
            # content = stopwords(content)
            Bunch.cat.append(cat)
            Bunch.contents.append(gram_3)
            categories_dict[cat]+=1
            print("So far: "+cat +" "+str(categories_dict[cat]))

    with open("./dat/"+temp_dat, "wb") as file_obj:
        pickle.dump(Bunch, file_obj)


def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def TFIDF(dat_name, trainset=False, testset=False, validset=False):
    dat = read_dat(dat_name)
    if trainset:
        tf_idf(dat,"train_tfidf.dat")
    elif testset:
        tf_idf(dat, "test_tfidf.dat", "train_tfidf.dat")
    elif validset:
        tf_idf(dat, "valid_tfidf.dat", "train_tfidf.dat")


def Embedding(dat_name):
    dat = read_dat(dat_name)
    Embed(dat,"train.dat","test.dat")


temp = files.get("val")
temp_dat = dat.get("val")


if __name__ == "__main__":
    # parse_dataset(temp, 600)
    # Embedding(temp_dat)
    TFIDF(temp_dat, trainset=True)
    # parse_val()