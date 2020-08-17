import sys
import traceback

import pymysql

from matching import AC_algorithm


class AnalyzeTopic():
    def __init__(self, topic, mysql_config):
        self.topic = topic
        self.mysql_config = mysql_config

    def search(self):
        # 连接数据库
        mysql_config = self.mysql_config
        db = pymysql.connect(**mysql_config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        sql = "SELECT text FROM topic"
        # 使用execute()方法执行SQL语句
        cursor.execute(sql)
        ac = AC_algorithm.AC()
        t = []
        result = []
        t.append(self.topic)
        ac.init(t)
        myresult = cursor.fetchall()
        for x in myresult:
            # print(x[0])
            a = ac.search(x[0])
            if a == 1:
                result.append(x[0])
        if len(result) != 0:
            generate_cloud(self.topic, result)
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
    wc.to_file('topic.png')


if __name__ == '__main__':
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'lab',
        'password': '123456',
        'db': 'weibo',
        'charset': 'utf8mb4'
    }
    keyword = '华晨宇'
    t = AnalyzeTopic(keyword, mysql_config)
    t.search()
