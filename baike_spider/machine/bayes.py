from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
import _pickle as pickle
import joblib
import numpy as np
import matplotlib.pyplot as plt


def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


trainpath = "train_tfidf.dat"
train_set = read_dat(trainpath)


testpath = "test_tfidf.dat"
test_set = read_dat(testpath)


clf = MultinomialNB(alpha=0.01)
clf.fit(train_set.tdm, train_set.cat)
# clf = joblib.load('./model/clf.pkl')
predicted = clf.predict(test_set.tdm)

# joblib.dump(clf, './model/clf.pkl')
from sklearn import metrics

label =['news_culture','news_edu','news_entertainment'
        ,'news_fashion','news_finance','news_food','news_health','news_military',
        'news_society','news_sports','news_tech','news_travel','science']
def metrics_result(actual, predict):
    print('acc:{0:.3f}'.format(metrics.precision_score(actual, predict, average='weighted')))
    c_matrix = confusion_matrix(actual, predicted, labels=label)
    return c_matrix


c_matrix = metrics_result(test_set.cat, predicted)
print(c_matrix)

import itertools
# 绘制混淆矩阵
def plot_confusion_matrix(cm, classes, normalize=True, title='Confusion matrix'):

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

plot_confusion_matrix(c_matrix,label)
