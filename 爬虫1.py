import requests

query = input("输入你要搜的关键词")
url = f"https://sogou.com/web?query={query}" 

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0."
}

resp = requests.get(url, headers=head)

print(resp)
print(resp.text)
