# -*- coding:utf-8 -*-

# X：两队的情况，该队比赛前的胜负状态
# Y：两队的胜负结果，胜负两类
# 只用逻辑回归得出线性分类
# 

import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

# 队员数据包括：每队每个人的各项指标
# 比赛数据包括：对战双方队伍、双方此前胜负情况（代表竞技状态）、结果
# 返回：双方队伍的综合指标，对战胜负
def build_dataset(teams, competitions, is_train = 1, need_y = 1):
    gt = teams.drop(['队员号'], axis=1).groupby('队名').mean().reset_index()
    gt['投篮准确率'] = gt['投篮命中次数'] / gt['投篮出手次数']
    # gt.to_csv('gt.csv')
    # merge会打乱顺序，只能手写
    if need_y:
        X = competitions.drop(['客场比分'], axis=1)
    else:
        X = competitions
    X['出场次数'] = 0.0
    X['首发次数'] = 0.0
    X['上场时间'] = 0.0
    X['投篮命中次数'] = 0.0
    X['投篮出手次数'] = 0.0
    X['三分命中次数'] = 0.0
    X['三分出手次数'] = 0.0
    X['罚球命中次数'] = 0.0
    X['罚球出手次数'] = 0.0
    X['篮板总数'] = 0.0
    X['前场篮板'] = 0.0
    X['后场篮板'] = 0.0
    X['助攻'] = 0.0
    X['抢断'] = 0.0
    X['盖帽'] = 0.0
    X['失误'] = 0.0
    X['犯规'] = 0.0
    X['得分'] = 0.0
    X['偏置'] = 1.0
    for i in range(len(competitions)):
        team1 = int(X['客场队名'].loc[i])
        team2 = int(X['主场队名'].loc[i])
        X.set_value(i, '出场次数', gt['出场次数'].loc[team1] - gt['出场次数'].loc[team2])
        X.set_value(i, '首发次数', gt['首发次数'].loc[team1] - gt['首发次数'].loc[team2])
        X.set_value(i, '上场时间', gt['上场时间'].loc[team1] - gt['上场时间'].loc[team2])
        X.set_value(i, '投篮命中次数', gt['投篮命中次数'].loc[team1] - gt['投篮命中次数'].loc[team2])
        X.set_value(i, '投篮出手次数', gt['投篮出手次数'].loc[team1] - gt['投篮出手次数'].loc[team2])
        X.set_value(i, '三分命中次数', gt['三分命中次数'].loc[team1] - gt['三分命中次数'].loc[team2])
        X.set_value(i, '三分出手次数', gt['三分出手次数'].loc[team1] - gt['三分出手次数'].loc[team2])
        X.set_value(i, '罚球命中次数', gt['罚球命中次数'].loc[team1] - gt['罚球命中次数'].loc[team2])
        X.set_value(i, '罚球出手次数', gt['罚球出手次数'].loc[team1] - gt['罚球出手次数'].loc[team2])
        X.set_value(i, '篮板总数', gt['篮板总数'].loc[team1] - gt['篮板总数'].loc[team2])
        X.set_value(i, '前场篮板', gt['前场篮板'].loc[team1] - gt['前场篮板'].loc[team2])
        X.set_value(i, '后场篮板', gt['后场篮板'].loc[team1] - gt['后场篮板'].loc[team2])
        X.set_value(i, '助攻', gt['助攻'].loc[team1] - gt['助攻'].loc[team2])
        X.set_value(i, '抢断', gt['抢断'].loc[team1] - gt['抢断'].loc[team2])
        X.set_value(i, '盖帽', gt['盖帽'].loc[team1] - gt['盖帽'].loc[team2])
        X.set_value(i, '失误', gt['失误'].loc[team1] - gt['失误'].loc[team2])
        X.set_value(i, '犯规', gt['犯规'].loc[team1] - gt['犯规'].loc[team2])
        X.set_value(i, '得分', gt['得分'].loc[team1] - gt['得分'].loc[team2])
    #X.to_csv('x.csv')
    if need_y:
        y = competitions['客场比分']
    else:
        y = np.ones(10)
    print 'Data ok'
    if is_train:
        return X.loc[:9000], y.loc[:9000]
    elif need_y:
        return X.loc[9000:], y.loc[9000:]
    else:
        return X, y

def prepare_csv(teamcsv, compcsv, is_train = 1, need_y = 1):
    print 'Prepareing csv data'
    teamdata = pd.read_csv(teamcsv)
    competitions = pd.read_csv(compcsv)
    # 初步处理比赛情况
    # 胜-负，为该队的比赛情况
    competitions['客场胜'] -= competitions['客场负']
    competitions['主场胜'] -= competitions['主场负']
    if need_y:
        # 比分相减，得到客场队伍的胜负情况
        competitions['客场比分'] -= competitions['主场比分']
        # delete unused column
        competitions = competitions.drop(['客场负','主场负','主场比分'], axis = 1)
    else :
        competitions = competitions.drop(['客场负','主场负'], axis = 1)
    return teamdata, competitions

if __name__ == '__main__':
    teamdata, competitions = prepare_csv('./teamData.csv', './matchDataTrain2.csv')
    X, y = build_dataset(teamdata, competitions)
    print X
    print y

