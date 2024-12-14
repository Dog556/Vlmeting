import requests
import yaml

filename ="config.yaml"
with open(filename,'r') as f:
    config = yaml.safe_load(f)

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Accept':'application/json'
}


def get_server(msg):
    key = config['key']
    url = f"{config['serverj']}{key}.send?title=最新CVE推送&desp={msg}"
    requests.get(url, headers=headers)
