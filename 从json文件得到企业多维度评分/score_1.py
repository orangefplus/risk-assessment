import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

def get_selected_fileds(type):
    if type=="Overall Network Rating" or type=="Basic Information Rating":
        selected_fields = [
            "tianyancha_score", "registered_capital", "paid_amount",
            "taxpayer_qualification", "enterprise_type"
        ]
    elif type=="Stability Rating":
        selected_fields = ["supplier", "invite", "limit_consumption"
                            ]
    elif type=="Risk Rating":
        selected_fields = [
            "penalize", "abnormal", "past_dishonest", "person_subject_to_execution"]
    elif type=="Innovation Rating":
        selected_fields = [
            "invite", "patent", "software_copyright", "copyright_works", 'tender']
    else:
        raise ValueError(f"Unknown rating type: {type}")

    return selected_fields
def get_features(fields,type,path):
    features=[]
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            file_path = os.path.join(path, filename)
            if filename =='四川澄华生物科技有限公司.json':
                pass
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            extracted_data = {
                "filename": filename,
                "company_name": data["company_name"],
                "company_id": data["company_id"]
            }
            if type=="Overall Network Rating" or type=="Basic Information Rating":
                if "basic_info" in data:
                    for field in fields:
                        extracted_data[field] = data["basic_info"].get(field, None)
            elif type == "Stability Rating":
                if "basic_info" in data:
                    if ('operating_term' in data["basic_info"]):
                        if (data["basic_info"]['operating_term']):
                            extracted_data["operating_term"] = data["basic_info"]["operating_term"]
                    else:
                        extracted_data["operating_term"] = np.nan
                for field in fields:
                    if field in data:
                        extracted_data[field] = len(data[field])
            elif type=="Risk Rating":
                for field in fields:
                    if field in data:
                        extracted_data[field] = len(data[field])
                if 'tax_rating' in data:
                    for item in data['tax_rating']:
                        if item["serial_number"] == '1':
                            extracted_data['tax_rating'] = item['taxpayer_credit_rating']
            elif  type=="Innovation Rating":
                for field in fields:
                    if field in data:
                        extracted_data[field] = len(data[field])
            else:
                raise ValueError(f"Unknown rating type: {type}")

            features.append(extracted_data)

    return pd.DataFrame(features)

def get_dict(type):
    taxpayer_qualification_dict = {
        '增值税一般纳税人': 8,
        '未知': 2,
        '一般纳税人转登记小规模纳税人': 6,
        '一般纳税人': 7,
        '其他': 4,
        '出口退（免）税企业': 9
    }
    enterprise_type_score_dict = {
        '有限责任公司(自然人投资或控股)': 7,
        '其他有限责任公司': 6,
        '有限责任公司(自然人独资)': 7,
        '有限责任公司（非自然人投资或控股的法人独资）': 5,
        '有限责任公司(自然人投资或控股的法人独资)': 5,
        '股份有限公司(非上市、自然人投资或控股)': 8,
        '其他股份有限公司(非上市)': 7,
        '有限责任公司（自然人投资或控股的法人独资）': 5,
        '有限责任公司(外商投资企业法人独资)': 8,
        '有限责任公司(中外合资)': 8,
        '股份有限公司(上市、自然人投资或控股)': 9,
        '有限责任公司（外商投资、非独资）': 7,
        '有限责任公司(外国法人独资)': 8,
        '有限责任公司(港澳台法人独资)': 8,
        '有限责任公司(台港澳与境内合资)': 7,
        '股份合作制': 5,
        '有限责任公司（港澳台投资、非独资）': 6,
        '其他股份有限公司(上市)': 9,
        '有限责任公司(国有控股)': 8,
        '股份有限公司(中外合资、未上市)': 7,
        '农民专业合作社': 4,
        '有限责任公司': 6,
        '有限责任公司分公司(自然人投资或控股)': 5,
        '股份有限公司(台港澳与境内合资、未上市)': 6,
        '股份有限公司(非上市、国有控股)': 7,
        '集体所有制': 4,
        '其他': 3,
        '有限责任公司(港澳台自然人独资)': 7,
        '有限责任公司(外商投资企业与内资合资)': 7,
        '有限责任公司(台港澳合资)': 7,
        '有限责任公司(外商合资)': 7,
        '有限责任公司分公司(自然人投资或控股的法人独资)': 5,
        '股份有限公司（港澳台投资、未上市）': 6,
        '有限责任公司(外商投资、非独资)': 7,
        '股份有限公司(上市、国有控股)': 9,
        '有限责任公司(非自然人投资或控股的法人独资)': 5,
        '有限责任公司(外国自然人独资)': 7,
        '个体工商户': 3,
        '有限合伙企业': 5,
        '未知': 2,
        '有限责任公司(中外合作)': 7
    }
    if type=="Overall Network Rating" or type=="Basic Information Rating":
        return taxpayer_qualification_dict,enterprise_type_score_dict

def processs_data_ONR_BIR(df):
    df['tianyancha_score'] = df['tianyancha_score'].str.slice(0, 2)
    df['registered_capital'] = df['registered_capital'].str.slice(0, -4)
    df['paid_amount'] = df['paid_amount'].str.slice(0, -4)
    df['filename'] = df['filename'].str.slice(0, -5)
    df['tianyancha_score'].replace('', np.nan, inplace=True)
    df['registered_capital'].replace('', np.nan, inplace=True)
    df['paid_amount'].replace('', np.nan, inplace=True)


    df['company_name'].fillna('四川航天电子设备研究所', inplace=True)
    mean_score = df['tianyancha_score'].astype(float).mean()
    df['tianyancha_score'].fillna(mean_score, inplace=True)
    df['registered_capital'].fillna(0, inplace=True)
    df['taxpayer_qualification'].replace('-', '未知', inplace=True)
    df['taxpayer_qualification'].fillna('未知', inplace=True)
    df['enterprise_type'].fillna('未知', inplace=True)

    return df
def score_registered_capital_ONR_BIR(value):
    if value <= 100:
        return 1
    elif value <= 200:
        return 2
    elif value <= 400:
        return 3
    elif value <= 550:
        return 4
    elif value <= 1000:
        return 5
    elif value <= 3010:
        return 6
    elif value <= 10000:
        return 7
    elif value <= 50000:
        return 8
    elif value <= 100000:
        return 9
    else:
        return 10
def map_rating_dict_ONR_BIR(df,type):
    dict1,dict2=get_dict(type)
    df['纳税人分数'] = (df['taxpayer_qualification'].map(dict1)) * 3
    df['企业类型评分'] = (df['enterprise_type'].map(dict2)) * 3
    df['registered_capital'] = pd.to_numeric(df['registered_capital'], errors='coerce')
    df['注册资本评分'] = (df['registered_capital'].apply(score_registered_capital_ONR_BIR)) * 4
    df['tianyancha_score'] = pd.to_numeric(df['tianyancha_score'], errors='coerce')
    df['全网评分'] = df['tianyancha_score']
    columns_to_sum = ['纳税人分数', '企业类型评分', '注册资本评分']
    df['基本信息评分'] = df[columns_to_sum].sum(axis=1)
    if type=="Overall Network Rating":
        rating = df[['company_name', 'company_id', '全网评分']]
    elif type=="Basic Information Rating":
        rating = df[['company_name', 'company_id', '基本信息评分']]
    else:
        raise ValueError(f"Unknown rating type: {type}")

    return rating

def score_SR(type_name, data):
    if type_name == "supplier":
        if data <= 10:
            return 10
        elif data <= 50:
            return 20
        elif data <= 100:
            return 30
        elif data <= 500:
            return 40
        else:
            return 50
    elif type_name == "invite":
        if data <= 10:
            return 10
        elif data <= 50:
            return 20
        elif data <= 100:
            return 30
        elif data <= 500:
            return 40
        else:
            return 50
    elif type_name == "limit_consumption":
        if data <= 1:
            return 50
        elif data <= 5:
            return 40
        elif data <= 10:
            return 30
        elif data <= 50:
            return 20
        else:
            return 10
    elif type_name == "date_period":
        if data <= 1000:
            return 10
        elif data <= 2000:
            return 20
        elif data <= 3000:
            return 30
        elif data <= 5000:
            return 40
        else:
            return 50
    else:
        raise ValueError(f"Unknown rating type: {type_name}")

def processs_data_SR(df):
    df['start_operating_term'] = df['operating_term'].str.slice(0, 10)
    df['over_operating_term'] = df['operating_term'].str.slice(start=11)
    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    df['over_operating_term'].replace('无固定期限', formatted_date, inplace=True)
    df['company_name'].fillna('四川航天电子设备研究所', inplace=True)
    df["start_operating_term"].fillna(formatted_date, inplace=True)
    df["operating_term"].fillna(formatted_date, inplace=True)
    df["over_operating_term"].fillna(formatted_date, inplace=True)
    df['start_operating_term'] = pd.to_datetime(df['start_operating_term'], errors='coerce')
    df['over_operating_term'] = pd.to_datetime(df['over_operating_term'], errors='coerce')
    df['over_operating_term'].fillna(pd.Timestamp(formatted_date), inplace=True)
    df['start_operating_term'].fillna(pd.Timestamp(formatted_date), inplace=True)
    df['date_period'] = (df['over_operating_term'] - df['start_operating_term']).dt.days

    df['supplier_score'] = df['supplier'].apply(lambda x: score_SR('supplier', x))
    df['invite_score'] = df['invite'].apply(lambda x: score_SR('invite', x))
    df['limit_consumption_score'] = df['limit_consumption'].apply(lambda x: score_SR('limit_consumption', x))
    df['date_period_score'] = df['date_period'].apply(lambda x: score_SR('date_period', x))

    # df[['supplier_score', 'invite_score', 'limit_consumption_score', 'date_period_score', 'total_score']] = df.apply(
    #     calculate_total_score_SR, axis=1, result_type='expand'
    # )

    df['total_score'] = df['supplier_score'] + df['invite_score'] + df['limit_consumption_score'] + df[
        'date_period_score']
    df['稳定性评分'] = df['total_score'] * 100 / 200
    score = df[['company_name','company_id','稳定性评分']]

    return score

def score_RR(type_name,value):
    if type_name=="penalize":
        if value == 0:
            return 20
        elif value == 1:
            return 10
        else:
            return 0
    elif type_name=="abnormal":
        if value == 0:
            return 20
        elif value == 1:
            return 10
        else:
            return 0
    elif type_name=="past_dishonest":
        if value < 1:
            return 20
        elif value <= 10:
            return 10
        elif value <= 50:
            return 5
        else:
            return 0
    elif type_name=="person_subject_to_execution":
        if value < 1:
            return 20
        elif value <= 2:
            return 15
        elif value <= 5:
            return 10
        elif value <= 10:
            return 5
        else:
            return 0
    elif type_name=="tax_rating":
        if value == 'A':
            return 20
        else:
            return 10
    else:
        raise ValueError(f"Unknown rating type: {type_name}")

def processs_data_RR(df):
    df['tax_rating'].fillna('未知', inplace=True)
    df['company_name'].fillna('四川航天电子设备研究所', inplace=True)

    df['行政处罚评分'] = df['penalize'].apply(lambda x: score_RR('penalize', x))
    df['异常经营评分'] = df['abnormal'].apply(lambda x: score_RR('abnormal', x))
    df['历史失信评分'] = df['past_dishonest'].apply(lambda x: score_RR('past_dishonest', x))
    df['历史被执行人评分'] = df['person_subject_to_execution'].apply(lambda x: score_RR('person_subject_to_execution', x))
    df['税务评分'] = df['tax_rating'].apply(lambda x: score_RR('tax_rating', x))

    columns_to_sum = ['行政处罚评分', '异常经营评分', '历史失信评分', '历史被执行人评分', '税务评分']
    df['风险评分'] = df[columns_to_sum].sum(axis=1)
    risk = df[['company_name', 'company_id', '风险评分']]
    return risk

def score_IR(type_name,value):
    if type_name=="patent":
        if value < 1:
            return 5
        elif value <= 5:
            return 10
        elif value <= 15:
            return 15
        else:
            return 20
    elif type_name=="software_copyright":
        if value < 5:
            return 5
        elif value <= 10:
            return 10
        elif value <= 15:
            return 15
        else:
            return 20
    elif type_name=="copyright_works":
        if value < 1:
            return 5
        elif value <= 10:
            return 10
        elif value <= 100:
            return 15
        else:
            return 20
    elif type_name=="tender":
        if value < 1:
            return 5
        elif value <= 10:
            return 10
        elif value <= 15:
            return 15
        else:
            return 20
    elif type_name == "invite":
        if value < 1:
            return 5
        elif value <= 5:
            return 10
        elif value <= 10:
            return 15
        else:
            return 20

    else:
        raise ValueError(f"Unknown rating type: {type_name}")

def processs_data_IR(df):
    df['company_name'].fillna('四川航天电子设备研究所', inplace=True)
    df['专利评分'] = df['patent'].apply(lambda x: score_IR('patent', x))
    df['软件著作评分'] = df['software_copyright'].apply(lambda x: score_IR('software_copyright', x))
    df['作品著作评分'] = df['copyright_works'].apply(lambda x: score_IR('copyright_works', x))
    df['招聘评分'] = df['invite'].apply(lambda x: score_IR('invite', x))
    df['招投标评分'] = df['tender'].apply(lambda x: score_IR('tender', x))

    columns_to_sum = ['专利评分', '软件著作评分', '作品著作评分', '招聘评分', '招投标评分']
    df['创新评分'] = df[columns_to_sum].sum(axis=1)

    innovation = df[['company_name', 'company_id', '创新评分']]
    return innovation

def Rating(type_name,input_path):
    fields=get_selected_fileds(type=type_name)
    feature=get_features(fields,type_name,path=input_path)

    if type_name=="Overall Network Rating" or type_name=="Basic Information Rating":
        df=processs_data_ONR_BIR(feature)
        df=map_rating_dict_ONR_BIR(df,type_name)
    elif type_name == "Stability Rating":
        df = processs_data_SR(feature)
    elif type_name=="Risk Rating":
        df = processs_data_RR(feature)
    elif type_name=="Innovation Rating":
        df = processs_data_IR(feature)

    return df




if __name__ == '__main__':
    input="../data"
    output="../output"

    if not os.path.isdir(output):
        os.makedirs(output)
        print(f"Directory {output} created.")
    else:
        print(f"The path {output} is already a directory.")
    types_list=["Overall Network Rating","Basic Information Rating",
                "Innovation Rating",
                "Stability Rating",
                "Risk Rating"]

    df_merged=Rating(types_list[0], input)
    for i in types_list[1:]:
        df_merged = pd.merge(df_merged, Rating(i, input), on=['company_name', 'company_id'], how='outer')
    df_merged.to_csv(output+"/score.csv", index=False)

    ##标准化
    # last_five_columns = df_merged.iloc[:, -5:]
    # scaler = MinMaxScaler()
    # normalized_data = scaler.fit_transform(last_five_columns)
    # normalized_df = pd.DataFrame(normalized_data, columns=last_five_columns.columns)
    # for i, column in enumerate(last_five_columns.columns):
    #     df_merged[column + '_normalized'] = normalized_df.iloc[:, i]
    # columns_to_drop = ['全网评分', '基本信息评分', '稳定性评分', '风险评分', '创新评分']
    # df_dropped = df_merged.drop(columns=columns_to_drop)
    # normalized_path = '../output/normalize_indicator.csv'
    # df_dropped.to_csv(normalized_path, index=False)

    print(f"{output}评分计算完成！！！！！！！")