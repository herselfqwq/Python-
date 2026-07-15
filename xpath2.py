from lxml import etree

tree = etree.parse("2.html")
# result = tree.xpath("/html")
# result = tree.xpath("/html/body/ul/li[1]/a/text()") #同层节点从1开始数！
# result = tree.xpath("/html/body/ol/li/a[@href = 'dapao']/text()")
# result = tree.xpath("/html/body/ol/li[2]/a/text()")
# ol_li_list = tree.xpath("/html/body/ol/li")
# for li in ol_li_list:
#     result = li.xpath("./a/text()") # 继续去寻找
#     print(result)
#     result2 = li.xpath("./a/@href")
#     print(result2)
# print(tree.xpath("/html/body/*/li/a/@href"))
print(tree.xpath("/html/body/div[1]/text()"))
