import re

#预加载正则表达式
# obj = re.compile(r"\d+")
# ret = obj.finditer("A的电话是10086，B的电话是10010")
# for it in ret :
#     print(it.group())

s = """
<div class='jay'></span id='1'>郭麒麟</span></div>
<div class='jj'></span id='2'>宋铁</span></div>
<div class='jolin'></span id='3'>大聪明</span></div>
<div class='sylar'></span id='4'>范思哲</span></div>
<div class='tory'></span id='5'>胡说八道</span></div>
"""
#.*?用来填空; re.S: 让.能匹配换行符; "?P<qwq>.*?把匹配到的东西丢到前面这个分组里"
obj = re.compile(r"<div class='.*?'></span id='(?P<id>\d+)'>(?P<qwq>.*?)</span></div>", re.S)

ret = obj.finditer(s)
for it in ret :
    print(it.group("qwq")+" "+it.group("id"))