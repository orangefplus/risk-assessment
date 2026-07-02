import json
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
filename = "newdataid/912newdata2.csv"  # 这里是包含公司名称的CSV文件
filepath = "newdataid/10text/text1"

# 百度大模型 API 凭证（请自行配置后再运行）
API_KEY = ""
SECRET_KEY = ""


def ask_Q(question, access_token):
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
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to obtain access token")

'''
def main():
    access_token = get_access_token()

    # 读取公司列表
    companies = pd.read_csv(filename)['company_name'].tolist()  # 假设CSV文件有一列名为“公司名称”

    for company in tqdm(companies):
        try:
            question = f"请先介绍一下{company}这家公司，然后再介绍一下他的信用代码和其他相关信息，同时重点关注风险信息"
            response = ask_Q(question, access_token)

            if response.status_code == 200:
                introduction = response.json().get("result", "")

                # 将结果写入以公司名命名的文本文件
                with open(f"{filepath}/{company}.text", "w", encoding="utf-8") as file:
                    file.write(introduction)
            else:
                print(f"Failed to fetch data for {company}: {response.status_code}")
        except Exception as e:
            print(f"Error processing {company}: {e}")


if __name__ == "__main__":
    main()
'''
def fetch_company_info(company, access_token):
    try:
        question = f"请先介绍一下{company}这家公司，然后再介绍一下他的信用代码和其他相关信息，同时重点关注风险信息"
        response = ask_Q(question, access_token)
        if response.status_code == 200:
            introduction = response.json().get("result", "")
            with open(f"{filepath}/{company}.text", "w", encoding="utf-8") as file:
                file.write(introduction)
            print(f"Successfully fetched data for {company}")
        else:
            print(f"Failed to fetch data for {company}: {response.status_code}")
    except Exception as e:
        print(f"Error processing {company}: {e}")
def main():
    access_token = get_access_token()
    companies = pd.read_csv(filename)['company_name'].tolist()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for company in tqdm(companies):
            executor.submit(fetch_company_info, company, access_token)

if __name__ == "__main__":
    main()