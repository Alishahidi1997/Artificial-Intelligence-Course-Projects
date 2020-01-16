import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


LABEL = 13
TARGET = "target"
NUM_OF_SUBSET = 5
NUM_OF_ATT = 5


def randomize_data(data):
    split = np.random.rand(len(data))
    train = data[split >= 0.2]
    test = data[split < 0.2]
    return train, test


def data_report(train_data, label):
    print('*'*20, '\n', label)
    print(train_data.groupby('target').age.count())
    print("Total ", len(train_data))


def classification(train_data, test_data):
    train_label = train_data[TARGET]
    train_data = train_data.drop('target', axis=1)

    test_label = test_data[TARGET]
    test_data = test_data.drop('target', axis=1)

    dt = DecisionTreeClassifier()
    dt.fit(train_data, train_label)
    pred = dt.predict(train_data)
    train_accuracy = accuracy_score(train_label, pred)

    pred = dt.predict(test_data)
    test_accuracy = accuracy_score(test_label, pred)

    return test_accuracy


def bagging(train_data, test_data):
    train_label = []
    test_label = test_data[TARGET]
    pred = []
    test_data = test_data.drop('target', axis=1)
    for i in range(NUM_OF_SUBSET):
        train_label.append(train_data[i][TARGET])
        train_data[i] = train_data[i].drop('target', axis=1)
        dt = DecisionTreeClassifier()
        dt.fit(train_data[i], train_label[i])
        pred.append(dt.predict(test_data[list(train_data[i].columns)]).tolist())

    counter = [0]*len(pred[0])
    for i in range(NUM_OF_SUBSET):
        for j in range(len(pred[0])):
            counter[j] += pred[i][j]

    bag_pred = []
    for j in range(len(pred[0])):
        if counter[j] > NUM_OF_SUBSET / 2:
            bag_pred.append(1)
        else:
            bag_pred.append(0)

    test_accuracy = accuracy_score(test_label, bag_pred)

    print("Random Forest accuracy score")
    print("\ttest:", test_accuracy)


def subset_gen(data):
    df_trimmed = []
    for i in range(NUM_OF_SUBSET):
        chosen_idx = np.random.choice(len(data), replace=False, size=150)
        df_trimmed.append(data.iloc[chosen_idx])
    return df_trimmed


def classification_one_att(train_data, test_data):
    test_accuracy = []
    min = 2
    index = -1
    orig_test_acc = classification(train_data, test_data)
    print("test accuracy without removing any attribute", orig_test_acc)
    for i in range(len(train_data.columns) - 1):
        train = train_data.drop([train_data.columns[i]], axis='columns')
        test = test_data.drop([test_data.columns[i]], axis='columns')
        test_accuracy.append(classification(train, test))
        if 0 <= orig_test_acc - test_accuracy[i] < min:
            min = orig_test_acc - test_accuracy[i]
            index = i
        print("test accuracy with removing", train_data.columns[i], " = ", test_accuracy[i])
    print("\nmin accuracy is resulted with removing ", train_data.columns[index], "  = ", test_accuracy[index])


def subset_gen_rand_att(train_data):
    df_trimmed = []
    for i in range(NUM_OF_SUBSET):
        data = train_data.drop('target', axis=1)
        data = data.sample(NUM_OF_ATT, axis=1)
        data.insert(len(data.columns), "target", train_data["target"])
        chosen_idx = np.random.choice(len(data), replace=False, size=150)
        df_trimmed.append(data.iloc[chosen_idx])
    return df_trimmed


data = pd.read_csv('data.csv')

train_data, test_data = randomize_data(data)
data_report(train_data, "Train Data")
data_report(test_data, "Test Data")

print('*' * 20, '\n', "Classification")
test_accuracy = classification(train_data, test_data)
print("Decision Tree accuracy score\n", "\ttest:", test_accuracy)

print('*' * 20, '\n', "Classification With Removing One Attribute")
classification_one_att(train_data, test_data)

print('*' * 20, '\n', "Bagging")
sub_data = subset_gen(train_data)
bagging(sub_data, test_data)

print('*' * 20, '\n', "Calculate accuracy of the decision tree with 5 random attributes")
data = train_data.drop('target', axis=1)
data = data.sample(NUM_OF_ATT, axis=1)
data.insert(len(data.columns), "target", train_data["target"])
columns = list(data.columns)
print("Columns = ", columns)

test_accuracy = classification(data, test_data[columns])
print("Decision Tree accuracy score\n", "\ttest:", test_accuracy)

print('*' * 20, '\n', "Calculate accuracy of the random forest with 5 random attributes")
print("Columns = ", columns)
sub_data = subset_gen(data)
bagging(sub_data, test_data[columns])

print('*' * 20, '\n', "Calculate accuracy of the random forest with 5 random attributes for each tree")
sub_data = subset_gen_rand_att(data)
for i in range(NUM_OF_ATT):
    print("Columns = ", list(sub_data[i].columns))
bagging(sub_data, test_data[columns])