#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import codecs
import csv
import json
import os
import random
import sys
import traceback
from time import sleep

import requests
from lxml import etree
from tqdm import tqdm


class Follow(object):
    def __init__(self, config):
        """Follow类初始化"""
        self.validate_config(config)
        self.write_mode = config[
            'write_mode']  # 结果信息保存类型，为list形式，可包含csv、mongo和mysql三种类型
        self.cookie = {'Cookie': config['cookie']}
        self.mysql_config = config.get('mysql_config')  # MySQL数据库连接配置，可以不填
        user_id_list = config['user_id_list']
        if not isinstance(user_id_list, list):
            if not os.path.isabs(user_id_list):
                user_id_list = os.path.split(
                    os.path.realpath(__file__))[0] + os.sep + user_id_list
            user_id_list = self.get_user_list(user_id_list)
        self.user_id_list = user_id_list  # 要爬取的微博用户的user_id列表
        self.user_id = ''
        self.follow_list = []  # 存储爬取到的所有关注微博的uri和用户昵称

    def validate_config(self, config):
        """验证配置是否正确"""
        user_id_list = config['user_id_list']
        if (not isinstance(user_id_list,
                           list)) and (not user_id_list.endswith('.txt')):
            sys.exit(u'user_id_list值应为list类型或txt文件路径')
        if not isinstance(user_id_list, list):
            if not os.path.isabs(user_id_list):
                user_id_list = os.path.split(
                    os.path.realpath(__file__))[0] + os.sep + user_id_list
            if not os.path.isfile(user_id_list):
                sys.exit(u'不存在%s文件' % user_id_list)
        # 验证write_mode
        write_mode = ['csv', 'json', 'mongo', 'mysql']
        if not isinstance(config['write_mode'], list):
            sys.exit(u'write_mode值应为list类型')
        for mode in config['write_mode']:
            if mode not in write_mode:
                sys.exit(
                    u'%s为无效模式，请从csv、json、mongo和mysql中挑选一个或多个作为write_mode' %
                    mode)

    def deal_html(self, url):
        """处理html"""
        try:
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_page_num(self):
        """获取关注列表页数"""
        url = "https://weibo.cn/%s/follow" % self.user_id
        selector = self.deal_html(url)
        if selector.xpath("//input[@name='mp']") == []:
            page_num = 1
        else:
            page_num = (int)(
                selector.xpath("//input[@name='mp']")[0].attrib['value'])
        return page_num

    def get_one_page(self, page):
        """获取第page页的user_id"""
        print(u'%s第%d页%s' % ('-' * 30, page, '-' * 30))
        url = 'https://weibo.cn/%s/follow?page=%d' % (self.user_id, page)
        selector = self.deal_html(url)
        table_list = selector.xpath('//table')
        if (page == 1 and len(table_list) == 0):
            print(u'cookie无效或提供的user_id无效')
        else:
            for t in table_list:
                im = t.xpath('.//a/@href')[-1]
                uri = im.split('uid=')[-1].split('&')[0].split('/')[-1]
                nickname = t.xpath('.//a/text()')[0]
                if {'uri': uri, 'nickname': nickname} not in self.follow_list:
                    self.follow_list.append({'user_id':self.user_id,'id': uri, 'screen_name': nickname})
                    print(u'%s %s %s' % (self.user_id, nickname, uri))

    def get_follow_list(self):
        """获取关注用户主页地址"""
        page_num = self.get_page_num()
        print(u'用户关注页数：' + str(page_num))
        page1 = 0
        random_pages = random.randint(1, 5)
        for page in tqdm(range(1, page_num + 1), desc=u'关注列表爬取进度'):
            self.get_one_page(page)

            if page - page1 == random_pages and page < page_num:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 5)

        print(u'用户关注列表爬取完毕')

    def write_to_txt(self):
        file_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'weibo_results/follow'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        with open(file_dir + self.user_id + '_follow_list.txt', 'ab') as f:
            for user in self.follow_list:
                f.write((user['user_id'] + ' ' + user['id'] + ' ' + user['screen_name'] + '\n').encode(
                    sys.stdout.encoding))

    def follow_to_csv(self):
        """将爬取到的用户信息写入csv文件"""
        file_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'weibo_results/follow'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + os.sep + self.user_id + '_follows.csv'
        result_headers = ['用户id', '关注者id', '昵称']
        result_data = [[v['user_id'],
                        v['id'], v['screen_name']]
                       for v in self.follow_list
                       ]
        self.csv_helper(result_headers, result_data, file_path)

    def csv_helper(self, headers, result_data, file_path):
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
        print(u'%s 关注信息写入csv文件完毕.' % self.user_id)
        print(file_path)

    def follow_to_mysql(self):
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
        self.mysql_create_database(mysql_config, create_database)
        # 创建'follow'表
        create_table = """
                CREATE TABLE IF NOT EXISTS follow (
                user_id varchar(20) NOT NULL,
                id varchar(20) NOT NULL,
                screen_name varchar(30),
                PRIMARY KEY (user_id,id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.mysql_create_table(mysql_config, create_table)
        self.mysql_insert(mysql_config, 'follow', self.follow_list)
        print(u'%s 关注信息写入MySQL数据库完毕' % self.user_id)

    def follow_to_database(self):
        """将用户信息写入文件/数据库"""
        self.write_to_txt()
        if 'csv' in self.write_mode:
            self.follow_to_csv()
        if 'mysql' in self.write_mode:
            self.follow_to_mysql()

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

    def get_user_list(self, file_name):
        """获取文件中的微博id信息"""
        with open(file_name, 'rb') as f:
            try:
                lines = f.read().splitlines()
                lines = [line.decode('utf-8-sig') for line in lines]
            except UnicodeDecodeError:
                sys.exit(u'%s文件应为utf-8编码，请先将文件编码转为utf-8再运行程序' % file_name)
            user_id_list = []
            for line in lines:
                info = line.split(' ')
                if len(info) > 0 and info[0].isdigit():
                    user_id = info[0]
                    if user_id not in user_id_list:
                        user_id_list.append(user_id)
        return user_id_list

    def initialize_info(self, user_id):
        """初始化爬虫信息"""
        self.follow_list = []
        self.user_id = user_id

    def start(self):
        """运行爬虫"""
        try:
            for user_id in self.user_id_list:
                self.initialize_info(user_id)
                print('*' * 100)
                self.get_follow_list()  # 爬取微博信息
                self.follow_to_database()
                print(u'信息抓取完毕')
                print('*' * 100)
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()


def main():
    try:
        config_path = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'config_follow.json'
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
            except ValueError:
                sys.exit(u'config.json 格式不正确.')
        wb = Follow(config)
        wb.start()  # 爬取微博信息

    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
