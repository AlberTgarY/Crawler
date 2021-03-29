import tensorflow as tf
import keras
import matplotlib.pyplot as plt
from keras.layers import Embedding
import numpy as np
import _pickle as pickle
from scipy.sparse import csr_matrix
import joblib
from keras.models import load_model

from sklearn.metrics import confusion_matrix

def read_dat(temp_dat):
    with open("./dat/"+temp_dat, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


trainpath = "train.dat"
train_set = read_dat(trainpath)

testpath = "test.dat"
test_set = read_dat(testpath)



cats = ['体育','娱乐','家居','房产','教育','时尚','时政','游戏','科技','财经']

train_cat_list = []
for cat in train_set.cat:
    train_cat_list.append(cats.index(cat))
print("done")
test_cat_list = []
for cat in test_set.cat:
    test_cat_list.append(cats.index(cat))
print("done")
# validpath = "train_test.dat"
# valid_set = read_dat(validpath)
# valid_cat_list = []
# for cat in valid_set.cat:
#     valid_cat_list.append(cats.index(cat))
# valid_cat = keras.utils.to_categorical(valid_cat_list, num_classes=10)
print("done")
# one-hot categories
train_cat = keras.utils.to_categorical(train_cat_list, num_classes=10)
test_cat = keras.utils.to_categorical(test_cat_list, num_classes=10)

data_dim = int(train_set.contents.shape[1])
print("done")


def get_model(data_dim):

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(5000, 100, input_length=data_dim))
    model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=128,  input_shape=(1, data_dim),return_sequences=True)))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(units=10, activation='softmax'))
    model.build((None, 1, data_dim))
    model.summary()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


model = get_model(data_dim)
history = model.fit(train_set.contents, train_cat,
                    epochs=2, batch_size=128,
                    validation_data=(test_set.contents, test_cat),
                    verbose=1,shuffle=True)
# model.evaluate(validset, valid_cat)
model.save('./model/model.h5')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','validation'], loc='upper right')
plt.show()


# model = load_model('./model/model.h5')
# predicted = model.predict(test_set.contents)

from sklearn import metrics
#
# def metrics_result(actual, predict):
#     predict = np.argmax(predict, axis=1)
#     c_matrix = confusion_matrix(actual, predict, labels=cats)
#
#     return c_matrix
#
# c_matrix = metrics_result(test_set.cat, predicted)
# print(c_matrix)
#
# import itertools
# # 绘制混淆矩阵
# def plot_confusion_matrix(cm, classes, normalize=True, title='Confusion matrix'):
#
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix, without normalization')
#     plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
#     plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45)
#     plt.yticks(tick_marks, classes)
#     fmt = '.2f' if normalize else 'd'
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt),
#                  horizontalalignment="center",
#                  color="white" if cm[i, j] > thresh else "black")
#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')
#     plt.show()
#
#
# plot_confusion_matrix(c_matrix, cats)