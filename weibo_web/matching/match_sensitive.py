import sys
import traceback

import pymysql

from matching import AC_algorithm


# class AnalyzeUser():
#     def __init__(self, user, mysql_config):
#         self.user = user
#         self.mysql_config = mysql_config
#
#     def search(self):
#         # 连接数据库
#         mysql_config = self.mysql_config
#         db = pymysql.connect(**mysql_config)
#         # 使用cursor()方法创建一个游标对象
#         cursor = db.cursor()
#         # 使用execute()方法执行SQL语句
#         sql = '''SELECT text FROM weibo WHERE screen_name like %s'''
#         params = ['%' + self.user + '%']
#         cursor.execute(sql,params)
#         #cursor.execute('SELECT text FROM weibo WHERE screen_name = %s', (self.user))
#         result = []
#         myresult = cursor.fetchall()
#         for x in myresult:
#             result.append(x[0])
#         if len(result) != 0:
#             generate_cloud(self.user, result)
#         else:
#             print("No data!")
#
#
# class AnalyzeTopic():
#     def __init__(self, topic, mysql_config):
#         self.topic = topic
#         self.mysql_config = mysql_config
#
#     def search(self):
#         # 连接数据库
#         mysql_config = self.mysql_config
#         db = pymysql.connect(**mysql_config)
#         # 使用cursor()方法创建一个游标对象
#         cursor = db.cursor()
#         sql = "SELECT text FROM topic"
#         # 使用execute()方法执行SQL语句
#         cursor.execute(sql)
#         ac = AC_algorithm.AC()
#         t = []
#         result = []
#         t.append(self.topic)
#         ac.init(t)
#         myresult = cursor.fetchall()
#         for x in myresult:
#             # print(x[0])
#             a = ac.search(x[0])
#             if a == 1:
#                 result.append(x[0])
#         if len(result) != 0:
#             generate_cloud(self.topic, result)
#         else:
#             print("No data!")


class AnalyzeSensitivity():
    def __init__(self, sensitive_word, mysql_config, table,field):
        self.sensitive = sensitive_word
        self.mysql_config = mysql_config
        self.table = table
        self.field=field

    def search(self):
        # 连接数据库
        ac = AC_algorithm.AC()
        t = []
        result = []
        for s in self.sensitive:
            # print(s)
            t.append(s)
        ac.init(t)
        mysql_config = self.mysql_config
        db = pymysql.connect(**mysql_config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        sql1 = "SELECT text,{field} FROM {table}".format(table=self.table,field=self.field)
        # sql2 = "SELECT text,user_id FROM topic"
        # 使用execute()方法执行SQL语句
        cursor.execute(sql1)
        myresult = cursor.fetchall()
        for x in myresult:
            a = ac.search(x[0])
            if a == 1:
                print(x[0])
                result.append({'id': x[1]})
        if len(result) != 0:
            self.sensitivity_to_mysql(result)
        else:
            print("No data!")
        # cursor.execute(sql2)
        # myresult = cursor.fetchall()
        # for x in myresult:
        #     a = ac.search(x[0])
        #     if a == 1:
        #         print(x[0])
        #         result.append({'id': x[1]})
        # if len(result) != 0:
        #     self.sensitivity_to_mysql(result)
        # else:
        #     print("No data!")

    # 与敏感关键词有关的id写入mysql
    def sensitivity_to_mysql(self, result):
        """将爬取的用户信息写入MySQL数据库"""
        mysql_config = self.mysql_config
        # 创建'weibo'数据库
        create_database = """CREATE DATABASE IF NOT EXISTS weibo DEFAULT
                                 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"""
        self.mysql_create_database(mysql_config, create_database)
        # 创建'sensitive'表
        create_table = """
                        CREATE TABLE IF NOT EXISTS sensitivity (
                        id varchar(20) NOT NULL,
                        PRIMARY KEY (id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.mysql_create_table(mysql_config, create_table)
        self.mysql_insert(mysql_config, 'sensitivity', result)
        print(u'敏感用户信息写入MySQL数据库完毕')

    def mysql_create_database(self, mysql_config, sql):
        """创建MySQL数据库"""
        try:
            import pymysql
        except ImportError:
            sys.exit(u'系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序')
        try:
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

        # if self.mysql_config:
        #     mysql_config = self.mysql_config
        mysql_config['db'] = 'weibo'
        connection = pymysql.connect(**mysql_config)
        self.mysql_create(connection, sql)

    def mysql_insert(self, mysql_config, table, data_list):
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


# def generate_cloud(key, result):
#     from wordcloud import WordCloud, STOPWORDS
#     import matplotlib.pyplot as plt
#     import jieba
#     # print(key)
#     jieba.suggest_freq(key, True)
#     result = ''.join(result)
#     res = jieba.cut(result)  # split chinese characters using jieba package
#     res_text = ' '.join(res)
#     background_img = plt.imread('../back.jpg')
#     STOPWORDS.add('../stopwords.txt')  # add stop words
#
#     # generate the word cloud
#     wc = WordCloud(background_color="white", mask=background_img, stopwords=STOPWORDS,
#                    font_path='../SourceHanSans-Bold.ttf').generate(res_text)
#
#     # show the image
#     plt.imshow(wc)
#     plt.axis('off')
#     plt.show()
#     wc.to_file('topic.png')


def main(param, table,field):
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'lab',
        'password': '123456',
        'db': 'weibo',
        'charset': 'utf8mb4'
    }

  #  param = ['快去']
    # if n == 1:
    #     u = AnalyzeUser(param, mysql_config)
    #     u.search()
    # elif n == 2:
    #     t = AnalyzeTopic(param, mysql_config)
    #     t.search()
    # else:
    s = AnalyzeSensitivity(param, mysql_config, table,field)
    s.search()
#
#
# if __name__ == '__main__':
#     keyword = '华晨宇'
#     user = '迪丽热巴'
#     sen = ['快去']
#     main(user, 1)
#     # main(keyword, 2)
#     # main(sen, 3)
