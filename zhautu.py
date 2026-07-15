#打开主页面源代码找到子页面地址
#通过href拿到子页面链接 img->src
import requests
from bs4 import BeautifulSoup
import time

header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0"
}
url = "https://www.umtuku.com/"
resp = requests.get(url, headers = header)
resp.encoding = "utf-8"
# print(resp.text)
main_page = BeautifulSoup(resp.text, "html.parser")
alist = main_page.find("div", class_ = "TypeList").find_all("a")
for a in alist:
    href = a.get("href")
    child_page_resp = requests.get(href, headers = header)
    child_page_resp.encoding = "utf-8"
    child_page_text = child_page_resp.text
    child_page = BeautifulSoup(child_page_text, "html.parser")
    p = child_page.find("p", align = "center")
    img = p.find("img")
    src = img.get("src")
    img_resp = requests.get(src)
    img_name = src.split("/")[-1] # 从后往前切割，根据/切割
    with open ("img/"+"img_name", mode = "wb") as f:
        f.write(img_resp.content)
    print("over" + " " + img.name)
    time.sleep(1)
print("over")
f.close()