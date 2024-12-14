import requests
from datetime import datetime
from database import db_json,insert_data,check_data_exists_in_db
import time
import json
import yaml
# 发送请求函数

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Accept':'application/json'
}

filename ="finger.yaml"
with open(filename,'r') as f:
    finger = yaml.safe_load(f)

with open("config.yaml",'r') as f:
    config = yaml.safe_load(f)
# api获取内容
def get_infos():
    nowtime = datetime.now().year
    url=f"https://api.github.com/search/repositories?q=CVE-{nowtime}&sort=updated"
    infos= requests.get(url,headers=headers)
    get_json=infos.json()
    extracted_data = []
    poc_name=finger['finger']
    try:
        for item in get_json['items']:
            description = item.get('description') or '' # 检测前判断是否为空
            description = description.lower()
            if any(poc.lower() in description for poc in poc_name):  # 使用生成器表达式检查任何关键词
                name_id = {
                    'title': item.get('name'),
                    'up_time': item.get('updated_at'),
                    'msg': item.get('description'),
                    'url': item.get('html_url')
                }
                extracted_data.append(name_id)

    except Exception as e:
        print(e)
        time.sleep(5)#异常休眠5s
    return extracted_data

def get_info():
    nowtime = datetime.now().year
    url=f"https://api.github.com/search/repositories?q=CVE-{nowtime}&per_page=20&sort=updated"
    infos= requests.get(url,headers=headers)
    get_json=infos.json()
    extracted_data = []
    try:
        for item in get_json['items']:
            name_id = {
                'title': item.get('name'),
                'up_time': item.get('updated_at'),
                'msg': item.get('description'),
                'url': item.get('html_url')
            }
            extracted_data.append(name_id)
    except Exception as e:
        print(e)
        time.sleep(5)
    return extracted_data

#获取发送数据格式
def send(datas):
    data = datas
    cve =[]
    for msg in data:
        new = f"> 编号:{msg['title']}\n\n> 时间:{msg['up_time']}\n\n> 内容:{msg['msg']}\n\n> url:{msg['url']}\n\n"
        cve.append(new)

    with open('CVE.log', 'w') as f:
        f.writelines(cve)
        f.close()
    return cve


def abc(datas):
    data = datas
    data2= db_json()
    # 检查是否有差异
    if not data or not data2:
        # 如果任一数据为空，将非空数据插入数据库
        if data:
            insert_data(data)
        elif data2:
            # 如果data2非空，也插入数据（这里可能不需要，取决于你的逻辑）
            insert_data(data2)
        print('数据库已更新') # 数据库已更新
    else:
        db_path = 'data.db'  # 数据库文件路径
        all_exist = check_data_exists_in_db(data, db_path)
        if all_exist:
            return True
        else:
            return False



def upload_file(file_path):
    # 定义上传接口的 URL
    url = config['upload_url']

    # 打开文件并读取内容
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        response = requests.post(url, files=files)
        # 检查响应状态
        if response.status_code == 200:
            # 解析 JSON 响应
            data = response.json()
            if data['status'] == 'success':
                print("upload success")
                print("Server：", data)
            else:
                print("Upload Error：", data['message'])
        else:
            print("Upload Error。")
            print("code：", response.status_code)

