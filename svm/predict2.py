# -*- coding:utf-8 -*-

# X：两队的情况，该队比赛前的胜负状态
# Y：两队的胜负结果，胜负两类
# 逻辑回归作为预测
# 

import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn import metrics
import build_data

def sigmoid(X, useStatus = True):  
    if useStatus:  
        return 1.0 / (1 + np.exp(-0.5 * float(X)));  
    else:  
        return float(X); 

if __name__ == '__main__':
    teamdata, competitions = build_data.prepare_csv('./teamData.csv', './matchDataTest.csv', 0, 0)
    X, y = build_data.build_dataset(teamdata, competitions, 0, 0)

    # 开始预测
    model = joblib.load('./model.m')
    pred = model.predict(X)
    result = np.zeros(len(pred))
    for i in range(len(pred)):
        result[i] = sigmoid(pred[i])
    pd.DataFrame({'abc':result}).to_csv('res.csv', index = False)
    #pd.DataFrame({'orig':orig, 'pred':pred}).to_csv('./res.csv')

