import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
import warnings


def randomize_data(data):
    split = np.random.rand(len(data))
    return data[split >= 0.2], data[split < 0.2]


def count_words(words_stats, train_frame):
    saadi_words_count = 0
    hafez_words_count = 0
    saadi_distich = 0
    hafez_distich = 0

    for _, row in train_frame.iterrows():
        words = word_tokenize(row["text"])
        if row['label'] == 'saadi':
            saadi_words_count += len(words)
            saadi_distich += 1
        else:
            hafez_words_count += len(words)
            hafez_distich += 1
        for word in words:
            if word not in words_stats:
                words_stats[word] = {'saadi': 0, 'hafez': 0}
            words_stats[word][row['label']] += 1

    return saadi_words_count, hafez_words_count, saadi_distich, hafez_distich


def prediction(data_frame, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich, laplas=False):
    predicts = []
    for _, row in data_frame.iterrows():
        saadi_p = saadi_distich / (saadi_distich + hafez_distich)
        hafez_p = hafez_distich / (saadi_distich + hafez_distich)
        words = word_tokenize(row["text"])
        for index, word in enumerate(words):
            if word in words_stats:
                if laplas:
                    saadi_p *= (words_stats[word]['saadi'] + 1) / (saadi_words_count + len(words_stats))
                    hafez_p *= (words_stats[word]['hafez'] + 1) / (hafez_words_count + len(words_stats))
                else:
                    saadi_p *= (words_stats[word]['saadi']) / (saadi_words_count)
                    hafez_p *= (words_stats[word]['hafez']) / (hafez_words_count)
        if saadi_p > hafez_p:
            predicts.append('saadi')
        else:
            predicts.append('hafez')
    data_frame['predict'] = pd.Series(predicts, index=data_frame.index)
    return data_frame


def prediction_report(data, label):
    saadi_distich = data[data['label'] == 'saadi']
    hafez_distich = data[data['label'] == 'hafez']

    correct_detected_hafez_frame = hafez_distich[hafez_distich['predict'] == 'hafez']
    correct_detected_saadi_frame = saadi_distich[saadi_distich['predict'] == 'saadi']

    accuracy = (len(correct_detected_hafez_frame) + len(correct_detected_saadi_frame)) / len(data)
    precision = len(correct_detected_hafez_frame) / len(data[data['predict'] == 'hafez'])
    recall = len(correct_detected_hafez_frame) / len(hafez_distich)

    print('*'*20, '\n', 'Report for', label)
    print('Recall:', recall)
    print('Precision:', precision)
    print('Accuracy:', accuracy)


def data_report(train_data, label):
    print('*'*20, '\n', label)
    print(train_data.groupby('label').count())
    print("Total ", len(train_data))


words_stats = {}
warnings.filterwarnings("ignore")

data = pd.read_csv('train_test.csv')
train_data, test_data = randomize_data(data)

data_report(train_data, "Train Data")
data_report(test_data, "Test Data")

saadi_words_count, hafez_words_count, saadi_distich, hafez_distich = count_words(words_stats, train_data)

prediction(train_data, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich)
prediction_report(train_data, 'Train Data')

prediction(test_data, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich)
prediction_report(test_data, 'Test Data')

ev_data = pd.read_csv('evaluate.csv')
ev_data_pre = prediction(ev_data, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich, laplas=True)
ev_data_pre.to_csv(r'./evaluation_output.csv', columns=['id', 'predict'], header=['id', 'label'], index=False)

prediction(train_data, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich, laplas=True)
prediction_report(train_data, 'Train Data + Laplas')

prediction(test_data, words_stats, saadi_words_count, hafez_words_count, saadi_distich, hafez_distich, laplas=True)
prediction_report(test_data, 'Test Data + Laplas')


