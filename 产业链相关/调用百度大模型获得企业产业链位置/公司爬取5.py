import os
import json
import requests
from tqdm import tqdm

# API_KEY 和 SECRET_KEY（请自行配置百度智能云控制台获取的 AK/SK 后再运行）
API_KEY = ""
SECRET_KEY = ""

# 文件夹路径，包含公司相关的json文件
folder_path = "./data(2)/data"
output_folder = "./result_29"  # 结果存储的文件夹


def ask_Q(question, access_token):
    """
    发送问题给百度AI接口，返回响应结果
    """
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to obtain access token")


def save_response_to_file(response_content, filepath, mode='a'):
    """
    保存API响应到文件中
    :param response_content: 响应内容
    :param filepath: 文件路径
    :param mode: 文件写入模式 ('w' for write, 'a' for append)
    """
    # 确保目录存在
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, mode, encoding='utf-8') as file:
        file.write(response_content)


def main():
    access_token = get_access_token()

    # 确保输出目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"文件夹已创建: {output_folder}")
    else:
        print(f"文件夹已存在: {output_folder}")

    # 用于存储所有提问结果的文件
    industry_output_file = f"{output_folder}/_29产业链分析.txt"

    # 定义产业链列表
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

    for chain in industry_chains:
        question = (
            f"请从专家的角度，为产业链“{chain}”列出其上游、中游、下游的内容，每个环节的回答请按照以下格式：\n"
            f"产业链标题：{chain}\n"
            "上游：...（上游环节简洁描述）\n"
            "中游：...（中游环节简洁描述）\n"
            "下游：...（下游环节简洁描述）\n\n"
            "注意：如果某个产业链的部分环节信息不明确或不存在，请用'N/A'表示。"
        )
        # 发送问题并将结果追加到同一个文件
        response = ask_Q(question, access_token)
        if response.status_code == 200:
            industry_chain_analysis = response.json().get("result", "")
            save_response_to_file(f"### 产业链：{chain} ###\n" + industry_chain_analysis + "\n\n", industry_output_file)  # 使用追加模式写入
        else:
            print(f"Failed to get analysis for {chain}: {response.status_code}")
            return

# 获取文件夹中的所有公司名（去除文件后缀.json）
    company_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    company_names = [os.path.splitext(f)[0] for f in company_files]

    # 问题7：循环遍历公司名，发送问题并获取公司所属的产业链及其位置
    for company in tqdm(company_names):
        try:
            # 构造问题
            question = (
                "请你以上述专家角度分析的29个产业链种类为基础，并且按照如下示例对公司进行产业链判断。"
                "公司名称：万岩铁路装备(成都)有限责任公司\n"
                "所属产业链：轨道交通\n"
                "所属产业链位置：中游\n"
                "当一个公司涉及多个产业链时，按照如下示例对公司进行产业链判断：\n"
                "公司名称：万岩铁路装备(成都)有限责任公司\n"
                "所属产业链1：轨道交通\n"
                "所属产业链1位置：中游\n"
                "所属产业链2：其他（即不包含在上述28个产业链中）\n"
                "所属产业链2位置：中游\n"
                "……\n"
                "除了公司名称，所属产业链，所属产业链位置，不要提供分析角度等其他文本\n"
                f"其中所属产业链必须包含在上面的29个分类中，即所属产业链应为{industry_chains}中的一个"
                f"公司名称：{company}"
            )
            response = ask_Q(question, access_token)

            if response.status_code == 200:
                company_industry_info = response.json().get("result", "")
                # 将公司信息保存到公司名命名的txt文件中
                save_response_to_file(company_industry_info, f"{output_folder}/{company}.txt", mode='w')
            else:
                print(f"Failed to fetch data for {company}: {response.status_code}")
        except Exception as e:
            print(f"Error processing {company}: {e}")

if __name__ == "__main__":
    main()
