import sys
import traceback

import pymysql

from matching import AC_algorithm


class AnalyzeUser():
    def __init__(self, user, mysql_config):
        self.user = user
        self.mysql_config = mysql_config

    def search(self):
        # 连接数据库
        mysql_config = self.mysql_config
        db = pymysql.connect(**mysql_config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        # 使用execute()方法执行SQL语句
        sql = '''SELECT text FROM weibo WHERE screen_name like %s'''
        params = ['%' + self.user + '%']
        cursor.execute(sql, params)
        # cursor.execute('SELECT text FROM weibo WHERE screen_name = %s', (self.user))
        result = []
        myresult = cursor.fetchall()
        for x in myresult:
            result.append(x[0])
        if len(result) != 0:
            generate_cloud(self.user, result)
        else:
            print("No data!")


def generate_cloud(key, result):
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.pyplot as plt
    import jieba
    # print(key)
    jieba.suggest_freq(key, True)
    result = ''.join(result)
    res = jieba.cut(result)  # split chinese characters using jieba package
    res_text = ' '.join(res)
    background_img = plt.imread('../back.jpg')
    STOPWORDS.add('../stopwords.txt')  # add stop words

    # generate the word cloud
    wc = WordCloud(background_color="white", mask=background_img, stopwords=STOPWORDS,
                   font_path='../SourceHanSans-Bold.ttf').generate(res_text)

    # show the image
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('user.png')


if __name__ == '__main__':
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'lab',
        'password': '123456',
        'db': 'weibo',
        'charset': 'utf8mb4'
    }
    user = '迪丽热巴'
    u = AnalyzeUser(user, mysql_config)
    u.search()
