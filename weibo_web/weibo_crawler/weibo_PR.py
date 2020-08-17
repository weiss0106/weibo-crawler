import re
import string
import sys
import os
import urllib
import urllib3
from bs4 import BeautifulSoup
import requests
from lxml import etree
import traceback


class weibo:
    cookie = {
        "Cookie": "ALF=1592475078; SCF=ArHI5GnyVVVZPduX1hkZ2sh-7JYvOzRb6A6PKY1oT9HYGLCXZtr_kbO0Z1m9rRk_ZfiqgJ0TY7Sx04wrCi4IOIw.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWksjWGNNPVOAJP0r0VVrjL5JpX5KMhUgL.FoMXSKM0Sh.pSKB2dJLoIEXLxK-LBo5L12qLxK-L12qLB-qLxKML1hnLBo2LxK.L1KnLB.qLxKqLBoBL1-zt; SUB=_2A25zx8CBDeRhGeFK7lUS9CfNzjiIHXVRS-DJrDV6PUJbkdANLXXakW1NQyjFTYSkY8rCCdikEbN1rFcjPjaFELoP; SUHB=0HThijoCLD1jBB; SSOLoginState=1589883089; _T_WM=55060150345; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174"
    }  # 将your cookie替换成自己的cookie

    # weibo类初始化
    def __init__(self, user_id, filter=0):

        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.userName = ''  # 用户名，如“Dear-迪丽热巴”
        self.weiboNum = 0  # 用户全部微博数
        self.weiboNum2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibos = []  # 微博内容
        self.num_zan = []  # 微博对应的点赞数
        self.num_forwarding = []  # 微博对应的转发数
        self.num_comment = []  # 微博对应的评论数
        self.pr = 0  # 用户的pagerank值

    # 获取用户昵称
    def getUserName(self):
        try:
            url = 'http://weibo.cn/%s/info' % (self.user_id)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            userName = selector.xpath("//title/text()")[0]
            self.userName = userName[:-3].encode('utf-8').decode('utf-8')
            print('用户昵称：', self.userName)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def getUserInfo(self):
        try:
            url = 'http://weibo.cn/u/%s?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weiboNum = num_wb
            print('微博数: ', str(self.weiboNum))

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print('关注数: ', str(self.following))

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print('粉丝数: ', str(self.followers))
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博内容及对应的点赞数、转发数、评论数
    def getWeiboInfo(self):
        try:
            url = 'http://weibo.cn/u/%s?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]') == []:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            pattern = r"\d+\.?\d*"
            # 微博内容
            for page in range(1, pageNum + 1):
                url2 = 'http://weibo.cn/u/%s?filter=%d&page=%d' % (self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=weibo.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        self.weiboNum2 = self.weiboNum2 + 1
                        print('正在爬取', self.userName, '的第', str(self.weiboNum2), '条微博')
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibos = str_t[0].xpath('string(.)').encode('gbk', 'ignore')
                        self.weibos.append(weibos)
                        # print '微博内容：'+ weibos
                        # 点赞数
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid = re.findall(pattern, str_zan, re.M)
                        num_zan = int(guid[0])
                        self.num_zan.append(num_zan)
                        # print '点赞数: ' + str(num_zan)
                        # 转发数
                        forwarding = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, forwarding, re.M)
                        num_forwarding = int(guid[0])
                        self.num_forwarding.append(num_forwarding)
                        # print '转发数: ' + str(num_forwarding)
                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        num_comment = int(guid[0])
                        self.num_comment.append(num_comment)
                        # print '评论数: ' + str(num_comment)
            if self.filter == 0:
                print('共', str(self.weiboNum2), '条微博')
            else:
                print('共', str(self.weiboNum), '条微博，其中', str(self.weiboNum2), '条为原创微博')
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 计算用户的pagerank值
    def getPR(self):
        sum_zan = sum(self.num_zan)
        sum_forwarding = sum(self.num_forwarding)
        sum_comment = sum(self.num_comment)
        self.pr = self.followers * 0.01 + (sum_zan + sum_forwarding * 100 + sum_comment * 30) * 1.0 / (
                self.weiboNum2 + 1)

    # 主程序
    def start(self):
        try:
            weibo.getUserName(self)
            weibo.getUserInfo(self)
            weibo.getWeiboInfo(self)
            weibo.getPR(self)
            print('信息抓取完毕')
            print('===========================================================================')
        except Exception as e:
            print("Error: ", e)

    # 将爬取的信息写入文件，非必需
    def writeTxt(self):
        try:
            if self.filter == 1:
                resultHeader = '\n\n原创微博内容：\n'
            else:
                resultHeader = '\n\n微博内容：\n'
            result = '用户信息\n用户昵称：' + self.userName + '\n用户id：' + str(self.user_id) + '\n微博数：' + str(
                self.weiboNum) + '\n关注数：' + str(self.following) + '\n粉丝数：' + str(self.followers) + resultHeader
            for i in range(1, self.weiboNum2 + 1):
                text = str(i) + ':' + self.weibos[i - 1] + '\n' + '点赞数：' + str(self.num_zan[i - 1]) + '	 转发数：' + str(
                    self.num_forwarding[i - 1]) + '	 评论数：' + str(self.num_comment[i - 1]) + '\n\n'
                result = result + text
            if os.path.isdir('../weibo') == False:
                os.mkdir('../weibo')
            f = open("weibo/%s.txt" % self.user_id, "wb")
            f.write(result)
            f.close()
            file_path = os.getcwd() + "/weibo" + "/%d" % self.user_id + ".txt"
            print('微博写入文件完毕，保存路径%s' % (file_path))
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


class mysql:
    def __init__(self, data_list):
        self.mysql_config = {}
        self.data_list = data_list

    def PR_to_mysql(self):
        """将爬取的用户信息写入MySQL数据库"""
        mysql_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'lab',
            'password': '123456',
            'charset': 'utf8mb4'
        }
        self.mysql_config = mysql_config
        # 创建'weibo'数据库
        create_database = """CREATE DATABASE IF NOT EXISTS weibo DEFAULT
                         CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"""
        self.mysql_create_database(mysql_config, create_database)
        # 创建'follow'表
        create_table = """
                CREATE TABLE IF NOT EXISTS PR (
                uid varchar(20) NOT NULL,
                PR varchar(30),
                PRIMARY KEY (uid)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.mysql_create_table(mysql_config, create_table)
        self.mysql_insert(mysql_config, 'PR', self.data_list)
        print(u'影响力信息写入MySQL数据库完毕')

    def mysql_create_database(self, mysql_config, sql):
        """创建MySQL数据库"""
        try:
            import pymysql
        except ImportError:
            sys.exit(u'系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序')
        try:
            if self.mysql_config:
                mysql_config = self.mysql_config
            connection = pymysql.connect(**mysql_config)
            self.mysql_create(connection, sql)
        except pymysql.OperationalError:
            sys.exit(u'系统中可能没有安装或正确配置MySQL数据库，请先根据系统环境安装或配置MySQL，再运行程序')

    def mysql_create(self, connection, sql):
        """创建MySQL数据库或表"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        finally:
            connection.close()

    def mysql_create_table(self, mysql_config, sql):
        """创建MySQL表"""
        import pymysql

        if self.mysql_config:
            mysql_config = self.mysql_config
        mysql_config['db'] = 'weibo'
        connection = pymysql.connect(**mysql_config)
        self.mysql_create(connection, sql)

    def mysql_insert(self, mysql_config, table, data_list):
        """向MySQL表插入或更新数据"""
        import pymysql

        keys = ', '.join(data_list[0].keys())
        values = ', '.join(['%s'] * len(data_list[0]))
        if self.mysql_config:
            mysql_config = self.mysql_config
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


def main(user_id):
    # 使用实例
    try:
        user_ids = user_id  # 替换成我们目标用户的id，可以改成任意合法的用户id（爬虫的微博id除外）
        user_pr = {}
        filter = 1  # 值为0表示爬取全部的微博信息（原创微博+转发微博），值为1表示只爬取原创微博
        users_pr_list = []
        for i in user_ids:
            wb = weibo(i, filter)  # 调用weibo类，创建微博实例wb
            wb.start()  # 爬取微博信息
            user_pr[i] = wb.pr  # 存储用户的pr值，用来判断用户的影响力，pr值越大代表影响力越高
            user_pr_dict = {'uid': i, 'PR': wb.pr}  # 获得用户id为i的pr值
            users_pr_list.append(user_pr_dict)
            # wb.writeTxt()  # wb.writeTxt()只是把信息写到文件里，大家可以根据自己的需要重新编写writeTxt()函数
        for i in user_ids:
            print('id为', i, '的用户的pr值为：', str(user_pr[i]))
        my_sql = mysql(users_pr_list)
        my_sql.PR_to_mysql()
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
