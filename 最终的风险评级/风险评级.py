import pandas as pd
import numpy as np
import os
df = pd.read_csv('score1.csv', index_col=None, encoding='gbk')
# 定义风险划分的函数
def classify_risk(risk_score):
    if risk_score >= 90:
        return 'A'
    elif risk_score >= 80:
        return 'B'
    elif risk_score >= 70:
        return 'C'
    elif risk_score >= 60:
        return 'D'
    else:
        return 'E'

# 应用风险划分函数
df['风险等级'] = df['风险评分'].apply(classify_risk)

# 输出结果
print(df[['company_name', '风险评分', '风险等级']])
c = df[['company_name', '风险评分', '风险等级']]
# 将结果保存到新的 CSV 文件
c.to_csv('classified_risk.csv', index=False)