from vector_unit import tf_idf,list_3_ngram
from sklearn.datasets import base
import _pickle as pickle


categories = ['news_culture','news_edu','news_entertainment','news_fashion','news_finance',
       'news_food','news_health','news_military','news_society','news_sports',
       'news_tech','news_travel','science']

categories_dict = {'news_culture':0,'news_edu':0,'news_entertainment':0,'news_fashion':0,'news_finance':0,
       'news_food':0,'news_health':0,'news_military':0,'news_society':0,'news_sports':0,
       'news_tech':0,'news_travel':0,'science':0}

files = {"cat": "all_cat.txt", "a": "dataset_aa.txt", "b": "dataset_ab.txt",
        "c": "dataset_ac.txt","d": "dataset_ad.txt", "e": "mlc_exmaple.txt"}

dat = {"a": "dataset_aa.dat", "b": "dataset_ab.dat",
        "c": "dataset_ac.dat","d": "dataset_ad.dat"}





def parse_dataset(temp,num=None):

    with open("./data/"+temp, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    Bunch = base.Bunch(cat=[], contents=[])
    count_ = 0
    for line in lines:
        t = ""
        cat = ""
        count = 0
        for element in line.split("|")[2:]:
            if len(element) > 1 and element != ",":
                if count == 0:
                    # print(element)
                    if "news_game" in element or "news_comic" in element:
                        cat = "news_entertainment"
                        # print("--news_entertainment")
                    if "digital" in element:
                        cat = "news_tech"
                        # print("--news_tech")
                    if "news_history" in element:
                        cat = "news_culture"
                        # print("--news_culture")
                    if "news_politics" in element:
                        cat = "news_society"
                    else:
                        for categorie in categories:
                            if categorie in element:
                                cat = categorie
                    count += 1
                else:
                    # print(element+"\n")
                    t = t + element
        gram_3 = list_3_ngram(t)
        if num:
            if count_ > int(num):
                break
        if len(gram_3[0]) != 0 and cat:
            Bunch.cat.append(cat)
            Bunch.contents.append(gram_3)
            count_ += 1
            print("So far: " + str(count_))


    with open("./dat/"+temp_dat, "wb") as file_obj:
        pickle.dump(Bunch, file_obj)


def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def count(temp_dat):
    cats = read_dat(temp_dat)
    count = 0
    for cat in cats.cat:
        if cat in categories:
            count += 1
            categories_dict[cat] = categories_dict[cat] + 1
    for cat in categories:
        # if int(categories_dict[cat])<10000:
            print(cat)
            print(categories_dict[cat])

def combine():
    Bunch = base.Bunch(cat=[], contents=[])
    aa = read_dat("dataset_aa.dat")
    ab = read_dat("dataset_ab.dat")
    ac = read_dat("dataset_ac.dat")
    # Bunch.cat = aa.cat + ab.cat
    # Bunch.contents = aa.contents + ab.contents
    Bunch.cat = aa.cat + ab.cat+ ac.cat
    Bunch.contents = aa.contents + ab.contents + ac.contents
    with open("./dat/dataset.dat", "wb") as file_obj:
        pickle.dump(Bunch, file_obj)


def TFIDF(dat_name, trainset=False, testset=False, validset=False):
    dat = read_dat(dat_name)
    if trainset:
        tf_idf(dat,"train_tfidf.dat")
    elif testset:
        tf_idf(dat, "test_tfidf.dat", "train_tfidf.dat")
    elif validset:
        tf_idf(dat, "valid_tfidf.dat", "train_tfidf.dat")



temp = files.get("d")
temp_dat = dat.get("d")

if __name__ == "__main__":
    # TFIDF("dataset_aa.dat", trainset=True)
    # TFIDF("dataset_ab.dat", testset=True)
    # TFIDF("dataset_ad.dat", validset=True)
    # combine()
    # parse_dataset(temp, num=3000)
    count("dataset.dat")
