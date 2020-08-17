import codecs
import csv
import datetime
import os
import sys
import traceback

import requests
import re
import bs4
import time

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
        result = []
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

                temp = [ranklist[i][0], ranklist[i][1], ranklist[i][2]]
                result.append(temp)
        print("\n")
        return result
    except:
        print("RankPrintError!")


# 热搜写入csv文件
def hotsearch_to_csv(result):
    """将爬取到的用户信息写入csv文件"""
    file_dir = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'weibo_results/hotsearch'
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    dtime = datetime.datetime.now()
    # print(dtime)
    un_time = time.mktime(dtime.timetuple())
    # print(un_time)
    file_path = file_dir + os.sep + str(un_time) + '_hotsearch.csv'
    result_headers = ['获取时间', '排名', '热搜内容', '搜索量']
    result_data = [[dtime, v[0],
                    v[1], v[2]]
                   for v in result
                   ]
    result_dict = [{'tnum':dtime.strftime("%Y-%m-%d %H:%M:%S"), 'id':v[0],
                    'content':v[1], 'hotindex':int(v[2])}
                   for v in result]
    # print(result_data)
    csv_helper(result_headers, result_data, file_path)
    return result_dict


def csv_helper(headers, result_data, file_path):
    """将指定信息写入csv文件"""
    if not os.path.isfile(file_path):
        is_first_write = 1
    else:
        is_first_write = 0
    if sys.version < '3':  # python2.x
        with open(file_path, 'ab') as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.writer(f)
            if is_first_write:
                writer.writerows([headers])
            writer.writerows(result_data)
    else:  # python3.x
        with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if is_first_write:
                writer.writerows([headers])
            writer.writerows(result_data)
    print(u'热搜信息写入csv文件完毕.')
    print(file_path)


# 热搜写入mysql
def hotsearch_to_mysql(result):
    """将爬取的用户信息写入MySQL数据库"""
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'lab',
        'password': '123456',
        'charset': 'utf8mb4'
    }
    # 创建'weibo'数据库
    create_database = """CREATE DATABASE IF NOT EXISTS weibo DEFAULT
                             CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"""
    mysql_create_database(mysql_config, create_database)
    # 创建'follow'表
    create_table = """
                    CREATE TABLE IF NOT EXISTS hotsearch (
                    tnum timestamp NOT NULL,
                    id varchar(20) NOT NULL,
                    content varchar(50),
                    hotindex INTEGER,
                    PRIMARY KEY (tnum,id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
    mysql_create_table(mysql_config, create_table)
    mysql_insert(mysql_config, 'hotsearch', result)
    print(u'热搜信息写入MySQL数据库完毕')



def mysql_create_database(mysql_config, sql):
    """创建MySQL数据库"""
    try:
        import pymysql
    except ImportError:
        sys.exit(u'系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序')
    try:
        connection = pymysql.connect(**mysql_config)
        mysql_create(connection, sql)
    except pymysql.OperationalError:
        sys.exit(u'系统中可能没有安装或正确配置MySQL数据库，请先根据系统环境安装或配置MySQL，再运行程序')


def mysql_create(connection, sql):
    """创建MySQL数据库或表"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    finally:
        connection.close()


def mysql_create_table(mysql_config, sql):
    """创建MySQL表"""
    import pymysql

    # if self.mysql_config:
    #     mysql_config = self.mysql_config
    mysql_config['db'] = 'weibo'
    connection = pymysql.connect(**mysql_config)
    mysql_create(connection, sql)


def mysql_insert( mysql_config, table, data_list):
    """向MySQL表插入或更新数据"""
    import pymysql

    keys = ', '.join(data_list[0].keys())
    values = ', '.join(['%s'] * len(data_list[0]))
    # if self.mysql_config:
    #     mysql_config = self.mysql_config
    mysql_config['db'] = 'weibo'
    connection = pymysql.connect(**mysql_config)
    cursor = connection.cursor()
    sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                                DUPLICATE KEY UPDATE""".format(table=table,
                                                               keys=keys,
                                                               values=values)
    update = ','.join([
        " {key} = values({key})".format(key=key)
        for key in data_list[0]
    ])
    sql += update
    try:
        cursor.executemany(
            sql, [tuple(data.values()) for data in data_list])
        connection.commit()
    except Exception as e:
        connection.rollback()
        print('Error: ', e)
        traceback.print_exc()
    finally:
        connection.close()


def main():
    try:
        # 微博热搜的网站
        url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
        # 使用二维列表存储每一条热搜信息的rank信息和内容
        rank = []
        text = getHTMLText(url)
        soup = HTMLTextconvert(text)
        HTMLSearch(soup, rank)
        result = Rankprint(rank, 51)
        result_data = hotsearch_to_csv(result)
        # print(result_data)
        hotsearch_to_mysql(result_data)

    except Exception as e:
        print("SystemError!", e)
        traceback.print_exc()
        return 0


if __name__ == '__main__':
    main()
