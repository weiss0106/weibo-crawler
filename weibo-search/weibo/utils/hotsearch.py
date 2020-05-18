import requests
import re
import bs4

# 获取一个中英文混合的字符串文本的字符宽度部分
widths = [
    (126, 1), (159, 0), (687, 1), (710, 0), (711, 1),
    (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
    (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1),
    (8426, 0), (9000, 1), (9002, 2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]


def get_width(a):
    global widths
    if a == 0xe or a == 0xf:
        return 0
    for num, wid in widths:
        if a <= num:
            return wid
    return 1


def length(str):
    sum = 0
    for ch in str:
        sum += get_width(ord(ch))
    return sum


# 获取HTML文本
def getHTMLText(url):
    try:
        # 模拟浏览器
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("InternetError!")
        return " "


# 解析并且返回HTML文本
def HTMLTextconvert(html):
    try:
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup
    except:
        print("HTMLConvertError!")
        return " "


# 检索HTML中的信息，获取搜索排名信息
# 存在置顶的情况，需要特殊判断
def HTMLSearch(html, ranklist):
    try:
        flag = 0
        # 找到所有tbody标签下的所有内容，并且遍历所有的儿子节点
        for tr in html.find("tbody").children:
            # 添加判断：获得的内容是否为标签Tag类型
            if isinstance(tr, bs4.element.Tag):
                # 使用flag特判置顶的情况
                if flag == 0:
                    rank = "置顶"
                    # 注意由于class属性会和python中的关键字重名，因此需要变为class_
                    td02 = tr.find_all(class_=re.compile('td-02'))
                    for i in td02:
                        if isinstance(i, bs4.element.Tag):
                            # trans得到的类型为列表
                            trans = i.find_all("a")
                    number = " "
                    ranklist.append([rank, trans[0].string, number])
                    flag = 1
                else:
                    # 排名信息在td标签下的class=td-01属性中
                    td01 = tr.find_all(class_=re.compile("td-01"))
                    for i in td01:
                        if isinstance(i, bs4.element.Tag):
                            rank = i.string
                    # 热搜内容和搜索量在td标签下的class=td-02属性中：内容是a标签，搜索量是span标签
                    td02 = tr.find_all(class_=re.compile("td-02"))
                    for i in td02:
                        name = i.find_all("a")
                        column = i.find_all("span")
                        # 使用string获取字符串信息不准确，因为微博还有一些热搜标题为含有表情的，因此使用了text
                    ranklist.append([rank, name[0].text, column[0].text])
    except:
        print("HTMLSearchError!")


# 打印排名
def Rankprint(ranklist, num):
    try:
        # 先打印表头,总长为70个字符，其中{1}和{3}是变化的空格数量计算，默认为：
        # 排名*4，空格*3，名称*50，空格*5，点击量*8
        a = " "
        print("——————————————————————————————————————")
        print("{0}{1}{2}{3}{4}\n".format("排名", a * 5, "热搜内容", a * 45, "搜索量" + a * 2))
        # 使用flag来判断是否输出了置顶内容
        flag = 0
        for i in range(num):
            if flag == 0:
                print("{0}{1}{2}\n".format(ranklist[i][0], a * 3, ranklist[i][1]))
                flag = 1
            else:
                # c是排名有一位、两位的数字，用来纠正空格
                c = 7 - len(ranklist[i][0])
                # 根据内容来随时计算所要填充的空格数量b
                str = ranklist[i][1]
                b = 62 - length(ranklist[i][1]) - len(ranklist[i][0]) - c
                print("{0}{1}{2}{3}{4:<8}".format(ranklist[i][0], a * c, ranklist[i][1], a * b, ranklist[i][2]))
        print("\n")
    except:
        print("RankPrintError!")


# 主函数
def main():
    try:
        # 微博热搜的网站
        url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
        # 使用二维列表存储每一条热搜信息的rank信息和内容
        rank = []
        text = getHTMLText(url)
        soup = HTMLTextconvert(text)
        HTMLSearch(soup, rank)
        Rankprint(rank, 51)
        return rank
    except:
        print("SystemError!")
        return 0


#main()
