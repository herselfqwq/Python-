#拿到网页源代码
#通过re提取信息
import requests
import re
import csv

f = open("data.csv", mode = "w", encoding = "utf-8")
csvwriter = csv.writer(f)
def run (now):
    url = f"https://movie.douban.com/top250?start={now}"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/ 150.0.0.0"
    }
    resp = requests.get(url, headers = header)
    page_content = resp.text
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<div class="bd">.*?<p>.*?<br>(?P<year>.*?)&nbsp.*?<span class="rating_num" property="v:average">(?P<rating>.*?)</span>.*?<span>(?P<sum>.*?)</span>', re.S)
    res = obj.finditer(page_content)
    for it in res :
    # print(it.group("name") + "," + it.group("year").strip() + "," + it.group("rating") + "," + it.group("sum"))
        dic = it.groupdict()
        dic["year"] = dic["year"].strip()
        csvwriter.writerow(dic.values())
for now in range(0, 226, 25):
    run(now)
print("over")
f.close()

