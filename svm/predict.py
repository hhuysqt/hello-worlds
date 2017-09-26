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
    teamdata, competitions = build_data.prepare_csv('./teamData.csv', './matchDataTrain2.csv')
    X, y = build_data.build_dataset(teamdata, competitions)

    # 开始预测
    model = joblib.load('./model.m')
    pred = model.predict(X)
    orig = y.values
    #pd.DataFrame({'orig':orig, 'pred':pred}).to_csv('./res.csv')

    # 正确率
    res = pred * orig
    total = 0
    corr = 0
    for r in res:
        if r > 0:
            corr += 1
        total += 1
    print 'total: ', total, ', corr: ', corr, ' , accuracy: ', float(corr)/total

    # AUC
    orig_clip = np.clip(orig, 0, 1)
    prop = np.ones(len(pred))
    for i in range(len(pred)):
        prop[i] = sigmoid(float(pred[i]))
    print 'AUC: ', metrics.roc_auc_score(orig_clip, prop)
