# -*- coding:utf-8 -*-
import build_data
import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn import svm

if __name__ == '__main__':
    teamdata, competitions = build_data.prepare_csv('./teamData.csv', './matchDataTrain2.csv')
    X, y = build_data.build_dataset(teamdata, competitions)

    # 开始训练
    print 'Start training'
    #model = LogisticRegression()
    model = svm.SVC()
    model.fit(X, y)

    print 'Done'
    joblib.dump(model, 'model.m')

