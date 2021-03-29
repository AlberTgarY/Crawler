import re
from stopwords import stopword
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.datasets import base
import _pickle as pickle
from scipy.sparse import csr_matrix
import numpy as np



def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def stopwords(news_content):
    stopwords = stopword()
    words_list = stopwords.Word_cut_list(news_content)
    return words_list


def Embed(dat, train_dat, test_dat):
    content = dat.contents
    temp_content =[]

    for i in content:
        temp = []
        for x in i[0].split(" "):
            temp.append(x)
        temp_content.append(temp)

    tokenizer = Tokenizer(num_words=5000,lower=True)
    tokenizer.fit_on_texts(temp_content)
    word_index = tokenizer.word_index
    Embeded = tokenizer.texts_to_sequences(temp_content)
    Embeded = pad_sequences(Embeded, maxlen=250)

    X_train, X_test, y_train, y_test = train_test_split(Embeded, dat.cat, test_size=0.20, random_state=42)
    train_Bunch = base.Bunch(cat=y_train, contents=X_train, vocabulary=word_index)
    test_Bunch = base.Bunch(cat=y_test, contents=X_test)
    with open("./dat/"+train_dat, "wb") as file_obj:
        pickle.dump(train_Bunch, file_obj)
    with open("./dat/" + test_dat, "wb") as file_obj:
        pickle.dump(test_Bunch, file_obj)


def list_3_ngram(news_content, n=3, m=2):
    gram_three = []
    # cut words
    words_list = stopwords(news_content)
    if len(words_list) < n:
        n = len(words_list)
    temp = [words_list[i - k:i] for k in range(m, n + 1) for i in range(k, len(words_list) + 1) ]

    for gram in temp:
        valid = True
        for word in gram:
            # get rid of the numbers
            if re.match(u"([\u0030-\u0039a])", word) or len(word) > 20:
                valid = False
                break
        if valid:
             gram_three.append(gram)
    dash = []
    dash.extend([' '.join(['_'.join(i) for i in gram_three])])
    return dash


def tf_idf(bunch, temp_dat, train_tfidf_path=None):
    temp = []
    idfBunch = base.Bunch(cat=bunch.cat, contents=bunch.contents, tdm=[], vocabulary=[])
    count, _count = 0, 0
    partial = []
    last =[]
    for content in bunch.contents:
        partial = partial+content
        last = partial
        count += 1
        if count // 2000 == 1:
            temp = temp + partial
            partial =[]
            count = 0
            _count += 1
            print(_count)
    temp = temp + last

    if train_tfidf_path is None:
        vectorizer = CountVectorizer()  # count frequency
        transformer = TfidfTransformer()  # tf-tdf weight
        freq = vectorizer.fit_transform(temp)  # freq.toarray() frequency array
        tfidf = transformer.fit_transform(freq)  # tfidf.toarray() tfidf matrix
        tfidf = csr_matrix(tfidf, dtype=np.float32)
        print(tfidf.shape)
        idfBunch.tdm = tfidf
        idfBunch.vocabulary = vectorizer.vocabulary_
    else:
        train_tfidfbunch = read_dat("train_tfidf.dat")
        idfBunch.vocabulary = train_tfidfbunch.vocabulary
        vectorizer = CountVectorizer(vocabulary=train_tfidfbunch.vocabulary)  # count frequency
        transformer = TfidfTransformer()  # tf-tdf weight
        freq = vectorizer.fit_transform(temp)  # freq.toarray() frequency array
        tfidf = transformer.fit_transform(freq)  # tfidf.toarray() tfidf matrix
        tfidf = csr_matrix(tfidf, dtype=np.float32)
        print(tfidf)
        idfBunch.tdm = tfidf

    with open("./dat/"+temp_dat, "wb") as file_obj:
        pickle.dump(idfBunch, file_obj)
