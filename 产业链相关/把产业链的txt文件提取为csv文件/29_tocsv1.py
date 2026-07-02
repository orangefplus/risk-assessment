import os
import csv
import re
from tqdm import tqdm  # 引入tqdm用于显示进度条

# 设定文件夹路径
folder_path = './result_29'  # 请修改为实际路径
csv_output = './result_29_company.csv'

# 创建正则表达式来匹配所需的字段
company_name_pattern = re.compile(r"公司名称：\s*(.*)")
industry_chain_pattern = re.compile(r"所属产业链：\s*(.*)")
industry_chain_location_pattern = re.compile(r"所属产业链位置：\s*(.*)")
industry_chain1_pattern = re.compile(r"所属产业链1：\s*(.*)")
industry_chain1_location_pattern = re.compile(r"所属产业链1位置：\s*(.*)")
industry_chain2_pattern = re.compile(r"所属产业链2：\s*(.*)")
industry_chain2_location_pattern = re.compile(r"所属产业链2位置：\s*(.*)")

# 打开CSV文件，准备写入数据
with open(csv_output, mode='w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # 写入CSV的表头
    csvwriter.writerow(['公司名称', '所属产业链', '所属产业链位置', '所属产业链1', '所属产业链1位置', '所属产业链2',
                        '所属产业链2位置'])

    # 遍历文件夹中的所有txt文件，并使用tqdm显示进度条
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt') and f != "_29产业链分析.txt"]

    for filename in tqdm(txt_files, desc="Processing files"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # 使用正则表达式提取各字段
            # company_name = company_name_pattern.search(content)
            company_name=os.path.splitext(filename)[0]
            industry_chain = industry_chain_pattern.search(content)
            industry_chain_location = industry_chain_location_pattern.search(content)
            industry_chain1 = industry_chain1_pattern.search(content)
            industry_chain1_location = industry_chain1_location_pattern.search(content)
            industry_chain2 = industry_chain2_pattern.search(content)
            industry_chain2_location = industry_chain2_location_pattern.search(content)

            # 提取值，若找不到则用'null'代替
            # company_name = company_name.group(1) if company_name else 'null'
            industry_chain = industry_chain.group(1) if industry_chain else 'null'
            industry_chain_location = industry_chain_location.group(1) if industry_chain_location else 'null'
            industry_chain1 = industry_chain1.group(1) if industry_chain1 else 'null'
            industry_chain1_location = industry_chain1_location.group(1) if industry_chain1_location else 'null'
            industry_chain2 = industry_chain2.group(1) if industry_chain2 else 'null'
            industry_chain2_location = industry_chain2_location.group(1) if industry_chain2_location else 'null'

            # 写入一行数据到CSV文件中
            csvwriter.writerow(
                [company_name, industry_chain, industry_chain_location, industry_chain1, industry_chain1_location,
                 industry_chain2, industry_chain2_location])

print(f"数据已成功写入到 {csv_output}")
