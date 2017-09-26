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
def build_dataset(teams, competitions, is_train = 1):
    grouped_teams = teams.drop(['队员号'], axis=1).groupby('队名').mean().reset_index()
    res_comp = pd.merge(competitions, grouped_teams, left_on='客场队名', right_on='队名')
    res_comp = pd.merge(res_comp, grouped_teams, left_on='主场队名', right_on='队名')
    res_comp['出场次数_x'] -= res_comp['出场次数_y']
    res_comp['首发次数_x'] -= res_comp['首发次数_y']
    res_comp['上场时间_x'] -= res_comp['上场时间_y']
    res_comp['投篮命中次数_x'] -= res_comp['投篮命中次数_y']
    res_comp['投篮出手次数_x'] -= res_comp['投篮出手次数_y']
    res_comp['三分命中次数_x'] -= res_comp['三分命中次数_y']
    res_comp['三分出手次数_x'] -= res_comp['三分出手次数_y']
    res_comp['罚球命中次数_x'] -= res_comp['罚球命中次数_y']
    res_comp['罚球出手次数_x'] -= res_comp['罚球出手次数_y']
    res_comp['篮板总数_x'] -= res_comp['篮板总数_y']
    res_comp['前场篮板_x'] -= res_comp['前场篮板_y']
    res_comp['后场篮板_x'] -= res_comp['后场篮板_y']
    res_comp['助攻_x'] -= res_comp['助攻_y']
    res_comp['抢断_x'] -= res_comp['抢断_y']
    res_comp['盖帽_x'] -= res_comp['盖帽_y']
    res_comp['失误_x'] -= res_comp['失误_y']
    res_comp['犯规_x'] -= res_comp['犯规_y']
    res_comp['得分_x'] -= res_comp['得分_y']
    X = res_comp.drop(['客场队名','主场队名','客场比分','队名_x','队名_y','出场次数_y','首发次数_y','上场时间_y','投篮命中次数_y','投篮出手次数_y','三分命中次数_y','三分出手次数_y','罚球命中次数_y','罚球出手次数_y','篮板总数_y','前场篮板_y','后场篮板_y','助攻_y','抢断_y','盖帽_y','失误_y','犯规_y','得分_y'], axis = 1)
    X['偏置'] = 1.0
    y = res_comp['客场比分']
    return X, y

def prepare_csv(teamcsv, compcsv):
    print 'Prepareing csv data'
    teamdata = pd.read_csv(teamcsv)
    competitions = pd.read_csv(compcsv)
    # 初步处理比赛情况
    # 胜-负，为该队的比赛情况
    competitions['客场胜'] -= competitions['客场负']
    competitions['主场胜'] -= competitions['主场负']
    # 比分相减，得到客场队伍的胜负情况
    competitions['客场比分'] -= competitions['主场比分']
    # delete unused column
    competitions = competitions.drop(['客场负','主场负','主场比分'], axis = 1)
    return teamdata, competitions

