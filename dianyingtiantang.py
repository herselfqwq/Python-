#定位到2026必看电影
#拿到子页面的链接
#进入链接拿到下载地址
import re
import requests
import csv

f = open("data.csv", mode = "w", encoding = "utf-8")
csvwriter = csv.writer(f)

domain = "https://www.dytt8899.com/" #记得ctrl+F查一下charset是哪种编码
resp = requests.get(domain) #去掉安全验证
resp.encoding = "gb2312" #指定字符集

obj1 = re.compile(r'2026必看热片.*?<ul>(?P<ul>.*?)</ul>', re.S)
obj2 = re.compile(r"<li><a href='(?P<url>.*?)' title=", re.S)
obj3 = re.compile(r'<title>【(?P<movie>.*?)】迅雷下载_电影天堂</title>.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)>magnet:', re.S)

res1 = obj1.finditer(resp.text)
url_list = []
for it in res1:
    ul = it.group("ul").strip()
    #提取子链接
    res2 = obj2.finditer(ul)
    for it2 in res2:
        #拼接，获得子页面连接
        url = domain + it2.group("url").strip('/')
        url_list.append(url)

#拿到ul里面的url
for url in url_list:
    resp2 = requests.get(url)
    resp2.encoding = "gb2312"
    res3 = obj3.search(resp2.text)
    dic = res3.groupdict()
    dic["download"] = dic["download"].strip('"')
    csvwriter.writerow(dic.values())
print("over")
f.close()
