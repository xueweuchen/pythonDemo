# -*- coding: utf-8 -*-
import pandas as pd
import csv as csv
import numpy as np
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV


def extract_feature(dataframe):
    dataframe['Gender'] = dataframe['Sex'].map(
        {'female': 0, 'male': 1}).astype(int)
    if len(dataframe.Embarked[dataframe.Embarked.isnull()]) > 0:
        dataframe.Embarked[dataframe.Embarked.isnull()] = \
            dataframe.Embarked.dropna().mode().values
    Ports_dict = {
        name: i for i, name in enumerate(np.unique(dataframe['Embarked']))}
    dataframe.Embarked = dataframe.Embarked.map(Ports_dict).astype(int)

    if True in dataframe.Age.isnull():
        dataframe.Age[dataframe.Age.isnull()] = dataframe.Age.dropna().median()

    if True in dataframe.Fare.isnull():
        dataframe.Fare[
            dataframe.Fare.isnull()] = dataframe.Fare.dropna().median()

    dataframe = dataframe.drop(
        ['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1)
    return dataframe.values

if __name__ == '__main__':
    train_df = pd.read_csv('train.csv', header=0)
    test_df = pd.read_csv('test.csv', header=0)
    ids = test_df['PassengerId'].values

    train_data = extract_feature(train_df)
    test_data = extract_feature(test_df)
    label_train = train_data[:, 0].astype(int)

    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4, 1e-5],
         'C': [1, 10, 100, 1000, 1500, 2000]}]

    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring='accuracy')
    clf.fit(train_data[:, 1:], label_train)
    print(clf.best_estimator_)

    result = clf.predict(test_data)

    with open("result.csv", 'w') as predictions_file:
        open_file_object = csv.writer(predictions_file)
        open_file_object.writerow(["PassengerId", "Survived"])
        open_file_object.writerows(zip(ids, result))
