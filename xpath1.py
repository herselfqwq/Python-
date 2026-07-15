#xpath是搜索内容的一门语言
#html是xml的一个子集
#xpath解析
from lxml import etree

xml = """
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <nick>臭豆腐</nick>
    <author>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="joy">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
        <div>
            <nick>惹了</nick>
        </div>
        <span>
            <nick>惹了2</nick>
        </span>
    </author>

    <partner>
        <nick id="ppc">胖胖陈</nick>
        <nick id="ppbc">胖胖不陈</nick>
    </partner>
</book>
"""

tree = etree.XML(xml)
# result = tree.xpath("/book/name/text()") # /book表示根节点, text()拿文本
# result = tree.xpath("/book/author/*/nick/text()") # *意味着任意节点，通配符
result = tree.xpath("/book//nick/text()")
print(result)