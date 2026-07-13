import requests

url = "https://fanyi.baidu.com/sug"
s = input("请输入你要翻译的词语")

fdata = {
    "kw" : s
}

#发送的数据放在字典中，传参

resp = requests.post(url, data = fdata)
print(resp.json()) # 处理成json