import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

# 读取CSV文件
df = pd.read_csv('score2(1).csv', index_col=None, encoding='gbk')

# 检查第三列及之后的列是否存在缺失值（NaN）
print("数据中的NaN值统计:")
nan_counts = df.iloc[:, 2:].isnull().sum()
print(nan_counts)

# 只对第三列及之后的列填充缺失值
for col in df.columns[2:]:
    if df[col].notnull().any():  # 如果列中有非NaN值，则计算平均值
        mean_val = df[col].mean(skipna=True)
        df[col] = df[col].fillna(mean_val)  # 直接赋值给原始DataFrame的列
    else:  # 如果列中全部是NaN，则用0填充
        df[col] = df[col].fillna(0)

# 再次检查缺失值是否已被填充
print("填充缺失值后的NaN值统计:")
nan_counts_after_fillna = df.iloc[:, 2:].isnull().sum()
print(nan_counts_after_fillna)

# 检查整个DataFrame中是否有完全相同的重复行
df = df.drop_duplicates()
duplicates_total = df.duplicated().sum()
print(f"整个数据集的重复行数: {duplicates_total}")

# 假设第一组列为权重25%，第二组列为权重75%
weight_25 = ['supplier_score', 'invite_score', 'limit_consumption_score', 'date_period_score',
             '行政处罚评分', '异常经营评分', '历史失信评分', '历史被执行人评分', '税务评分']  # 需要权重25%的列名
weight_75 = [col for col in df.columns[2:] if col not in weight_25]  # 其他列为权重75%

# 应用权重
for col in weight_25:
    df[col] *= 0.25

for col in weight_75:
    df[col] *= 0.75

# 行归一化
scaler = MinMaxScaler()
features = df.iloc[:, 2:].values
features_normalized = scaler.fit_transform(features)

# 使用PCA降维至10维
pca = PCA(n_components=10)
features_pca = pca.fit_transform(features_normalized)

# 计算降维后的欧几里得距离矩阵
distance_matrix = euclidean_distances(features_pca)

# 使用倒数转换法将距离转换为相似度
similarity_matrix = 1.0 / (distance_matrix + 1.0)

# 创建一个结果DataFrame，用于保存相似度结果
result = []

# 遍历每家公司，计算与其他公司的相似度
for i in range(len(df)):
    company_name = df.iloc[i, 0]  # 获取公司的名字
    company_id = df.iloc[i, 1]  # 获取公司的ID
    similarity_scores = list(enumerate(similarity_matrix[i]))  # 获取该公司与所有其他公司的相似度
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)  # 按相似度从高到低排序
    # 选取除自身外的一些公司，自身排第一个
    top_similarities = similarity_scores[1:10]

    # 获取相似公司的名字、ID和相似度
    top_5 = []
    flag = 0
    # 选5个公司
    for idx, score in top_similarities:
        if flag == 5:
            break
        if df.iloc[idx, 1] != company_id:
            flag = flag + 1
            top_5.append(df.iloc[idx, 0])  # 相似公司的名字
            top_5.append(df.iloc[idx, 1])  # 相似公司的ID
            top_5.append(score)  # 相似度得分

    result.append([company_name, company_id] + top_5)

# 将结果转换为DataFrame并保存为CSV
result_df = pd.DataFrame(result, columns=['公司名', '公司ID', '最相似公司1', '最相似ID1', '相似度1',
                                          '最相似公司2', '最相似ID2', '相似度2',
                                          '最相似公司3', '最相似ID3', '相似度3',
                                          '最相似公司4', '最相似ID4', '相似度4',
                                          '最相似公司5', '最相似ID5', '相似度5'])

# 输出结果到CSV文件
result_df.to_csv('company_similarity_results.csv', index=False)

# 打印结果
print(result_df.head())