import pandas as pd

# List of valid industry chains
industry_chains = [
    "集成电路", "新型显示", "智能终端", "高端软件与操作系统",
    "大数据与人工智能（含车载智能控制系统）", "工业互联网",
    "卫星互联网与卫星应用", "金融科技", "航空发动机",
    "工业无人机", "大飞机制造与服务", "汽车（新能源汽车）",
    "轨道交通", "现代物流", "生态环保",
    "新能源", "新材料", "创新药（含中医药）",
    "高端医疗器械", "高端诊疗", "旅游业",
    "文创业（含数字文创）", "会展业", "体育产业", "音乐产业",
    "美食产业（含绿色食品）", "现代种业", "都市农业", "其他"
]

# Load the CSV file into a DataFrame
df = pd.read_csv('result_29_company_v2.csv')

# Define a function to check if a value belongs to the list, otherwise append the original value in parentheses
def check_industry(value):
    if pd.notna(value) and value not in industry_chains:
        # return f'其他（{value}）'  # Replace with '其他（original value）'
        return '其他'
    return value

df['所属产业链1'] = df['所属产业链1'].replace("大数据与人工智能", "大数据与人工智能（含车载智能控制系统）")
df['所属产业链1'] = df['所属产业链1'].replace("新能源汽车", "汽车（新能源汽车）")
df['所属产业链1'] = df['所属产业链1'].replace("生物医药（创新药含中医药）", "创新药（含中医药）")
df['所属产业链1'] = df['所属产业链1'].replace("创新药（含中医药", "创新药（含中医药）")
df['所属产业链1'] = df['所属产业链1'].replace("中药产业（归为创新药（含中医药））", "创新药（含中医药）")
df['所属产业链1'] = df['所属产业链1'].replace("生物医药（属于创新药（含中医药）的细分领域）", "创新药（含中医药）")

df['所属产业链1'] = df['所属产业链1'].replace("现代农业（归类于都市农业）", "都市农业")
df['所属产业链1'] = df['所属产业链1'].replace("现代农业（属于都市农业范畴）", "都市农业")
df['所属产业链1'] = df['所属产业链1'].replace("生物医药（属于创新药（含中医药）的广义范畴）", "创新药（含中医药）")
df['所属产业链1'] = df['所属产业链1'].replace("其他（即不包含在上述29个产业链中）", "其他")
df['所属产业链1'] = df['所属产业链1'].replace("其他（即不包含在上述28个产业链中）", "其他")
df['所属产业链1'] = df['所属产业链1'].replace("新能源（如果公司涉及煤炭勘探并致力于新能源开发或煤炭清洁利用技术）", "新能源")
df['所属产业链1'] = df['所属产业链1'].replace("智能终端智能终端", "智能终端")
df['所属产业链1'] = df['所属产业链1'].replace("现代农业（可归类为都市农业）", "都市农业")

df['所属产业链1'] = df['所属产业链1'].replace("现代物流（考虑到质量检测服务在物流链条中的关键性，尤其是在确保运输物资质量与安全方面，可以将其归类为现代物流产业链的一部分）", "现代物流")
df['所属产业链1'] = df['所属产业链1'].replace("现代农业（归为都市农业）", "都市农业")
df['所属产业链1'] = df['所属产业链1'].replace("现代农业（属于“都市农业”的广义范畴）", "都市农业")
df['所属产业链1'] = df['所属产业链1'].replace("现代物流（考虑到建筑装饰工程可能涉及物流运输环节，特别是材料采购与配送）", "现代物流")
df['所属产业链1'] = df['所属产业链1'].replace("现代物流业", "现代物流")
df['所属产业链1'] = df['所属产业链1'].replace("现在农业现代种业", "现代种业")




# Apply the function to the '所属产业链1' column
df['所属产业链1'] = df['所属产业链1'].apply(check_industry)

# Replace "大数据与人工智能" with "大数据与人工智能（含车载智能控制系统）"
# df['所属产业链1'] = df['所属产业链1'].replace("大数据与人工智能", "大数据与人工智能（含车载智能控制系统）")

# Save the updated DataFrame to a new CSV file
df.to_csv('./result_29_company_v3.csv', index=False)
