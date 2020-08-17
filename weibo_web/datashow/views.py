import csv
import json
import os
import sys
import traceback
from os import path

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from datashow.models import *
from weibo_crawler.weibo_PR import main
from weibo_crawler.weibo_comment import WeiboLogin, comment_path, get_cookies, start_crawl, comment_to_mysql, \
    text_to_txt, generate_cloud
from weibo_crawler.weibo_user import Weibo
from weibo_crawler.weibo_follow import Follow
from weibo_crawler import weibo_hotsearch
from matching import match_sensitive
from weibo_web import settings
from datashow.mail import sendmail


def index(request):
    """显示首页"""
    return render(request, 'index.html')


def user_config(request):
    return render(request, 'user_config_form.html')


def user_results(request):
    """用户微博爬取"""
    user_id_list = []
    user_id_list.append(request.POST.get('uid_list'))
    filter = request.POST.get('filter')
    since_date = request.POST.get('d')
    opd = request.POST.get('opd')
    rpd = request.POST.get('rpd')
    ovd = request.POST.get('ovd')
    rvd = request.POST.get('rvd')
    cur = connection.cursor()
    cur.execute('DROP TABLE weibo')
    try:
        config_path = 'D:/Python/lab_weibo/weibo_web/weibo_crawler/config_user.json'
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config_user.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
                """后台赋值"""
                config['user_id_list'] = user_id_list
                config['filter'] = int(filter)
                config['since_date'] = since_date
                config['original_pic_download'] = int(opd)
                config['retweet_pic_download'] = int(rpd)
                config['original_video_download'] = int(ovd)
                config['retweet_video_download'] = int(rvd)
            except ValueError:
                sys.exit(u'config.json 格式不正确')
        wb = Weibo(config)
        wb.start()  # 爬取微博信息
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()
    # 获取用户信息
    # cur = connection.cursor()
    cur.execute('SELECT id, screen_name FROM user')

    selected1 = cur.fetchall()
    user = []
    for item in selected1:
        user.append((item[0], item[1]))
    # 获取微博信息
    cur.execute('SELECT id,text,created_at,attitudes_count,comments_count FROM weibo')
    selected2 = cur.fetchall()
    weibo_list = []
    for item in selected2:
        weibo_list.append((item[0], item[1], item[2], item[3], item[4]))
    # 计算pr值
    main(user_id_list)
    # 将用户pr值添加到用户信息中
    cur.execute('SELECT PR FROM pr WHERE uid = %s', (user_id_list[0]))
    selected3 = cur.fetchall()
    # pr=[]
    i = 0
    for item in selected3:
        temp = user[i]
        temp = temp + item
        user[i] = temp
        i += 1
    context = {
        'user': user,
        # 'screen_name': screen_name,
        'weibo_list': weibo_list,
        # 'pr':pr,
    }
    return render(request, 'user_results.html', context)


def topic_results(request):
    # keyword = request.POST.get('keyword')
    # startTime = request.POST.get('startTime')
    # endTime = request.POST.get('endTime')
    # url = 'http://127.0.0.1:6800/schedule.json'
    # data = {'project': 'weibo_keyword', 'spider': 'search', 'keyword': keyword, 'startTime': startTime,
    #         'endTime': endTime}
    # print(requests.post(url=url, data=data))
    # requrl = "http://localhost:6800/listjobs.json?project=weibo_keyword"
    # requests.get(requrl)
    cur = connection.cursor()
    cur.execute(
        'SELECT user_id, screen_name,text, created_at, attitudes_count, comments_count,reposts_count FROM topic')
    selected = cur.fetchall()
    topic_list = []
    for item in selected:
        topic_list.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    context = {
        'topic_list': topic_list,
        # 'keyword': keyword,
    }
    return render(request, 'topic_results.html', context)


def comment_config_form(request):
    return render(request, 'comment_config_form.html')


def comment_results(request):
    """处理登录以及输入验证码"""
    username = "13284092231"  # 用户名（注册的手机号）
    password = "990411"  # 密码
    cookie_path = "Cookie.txt"  # 保存cookie 的文件名称
    id = request.POST.get('id')
    cur = connection.cursor()
    cur.execute('DROP TABLE comment')
    WeiboLogin(username, password, cookie_path).login()
    with open('{}/{}.csv'.format(comment_path, id), mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['id', 'wid', 'time', 'text', 'like_count', 'uid', 'username', 'following', 'followed', 'pro_url'])
    result, text = start_crawl(get_cookies(), id)
    comment_to_mysql(result, id)
    text_to_txt(text, id)
    generate_cloud(id)

    cur.execute(
        'SELECT time,uid,username,text,like_count,following,followed FROM comment')
    selected = cur.fetchall()
    comment_list = []
    for item in selected:
        comment_list.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    context = {
        'wid': id,
        'comment_list': comment_list,
        # 'keyword': keyword,
    }
    return render(request, 'comment_results.html', context)


def follow_config(request):
    return render(request, 'follow_config_form.html')


def follow_results(request):
    user_id_list = []
    user_id_list.append(request.POST.get('uid_list'))
    try:
        filename = 'config_follow.json'
        config_path = os.path.join(settings.BASE_DIR, "weibo_crawler/{}".format(filename))
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
                config['user_id_list'] = user_id_list
            except ValueError:
                sys.exit(u'config.json 格式不正确.')
        wb = Follow(config)
        wb.start()  # 爬取微博信息
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()
    uid = user_id_list
    follow = []
    cur = connection.cursor()
    cur.execute('SELECT id,screen_name FROM follow')
    selected = cur.fetchall()
    for item in selected:
        follow.append((item[0], item[1]))
    context = {
        'uid': user_id_list,
        'follow_list': follow,
    }
    return render(request, 'follow_results.html', context)


def hotsearch_result(request):
    cur = connection.cursor()
    cur.execute('DROP TABLE hotsearch')
    weibo_hotsearch.main()
    cur.execute('SELECT id,tnum,content,hotindex FROM hotsearch ORDER BY id')
    hotsearch = []
    selected = cur.fetchall()
    for item in selected:
        hotsearch.append((int(item[0]), item[1], item[2], item[3]))
    hotsearch_list = sorted(hotsearch)
    context = {
        'hotsearch': hotsearch_list,
    }
    return render(request, 'hotsearch_results.html', context)


def weibo_filter(request):
    if request.method == "GET":
        return render(request, "sensitivity.html")
    elif request.method == "POST":
        sen = request.POST.get("word")
        cur = connection.cursor()
        cur.execute('SELECT id,text,created_at,attitudes_count,comments_count FROM weibo')
        selected = cur.fetchall()
        weibo_list = []
        for item in selected:
            weibo_list.append((item[0], item[1], item[2], item[3], item[4]))

        cur.execute('SELECT id, screen_name FROM user')
        selected1 = cur.fetchall()
        user = []
        user_id_list = []
        for item in selected1:
            user.append((item[0], item[1]))
            user_id_list.append(item[0])

        # 将用户pr值添加到用户信息中
        cur.execute('SELECT PR FROM pr WHERE uid = %s', (user_id_list[0]))
        selected3 = cur.fetchall()
        # pr=[]
        i = 0
        for item in selected3:
            temp = user[i]
            temp = temp + item
            user[i] = temp
            i += 1
        # if request.method == "GET":
        #     return render(request, "sensitivity.html")
        # elif request.method == "POST":
        #     sen = request.POST.get("word")
        #     # return render(request,"popup_response.html",{"sen":sen})
        cur.execute('DROP TABLE sensitivity')
        sensitive = []
        sensitive.append(sen)
        match_sensitive.main(sensitive, 'weibo', 'id')
        cur.execute('SELECT id FROM sensitivity')
        sensitive_id = cur.fetchall()
        mailbody = ''
        for item in sensitive_id:
            mailbody += item[0].__str__() + '\n'
        sendmail('1170301026@stu.hit.edu.cn', '敏感内容id', mailbody)
        i = 0
        for w in weibo_list:
            id = w[0]
            for item in sensitive_id:
                if id == item[0]:
                    weibo_list.remove(w)
        context = {
            'user': user,
            'weibo_list': weibo_list,
        }
        return render(request, "user_results.html", context)


def comment_filter(request):
    if request.method == "GET":
        return render(request, "sensitivity.html")
    elif request.method == "POST":
        sen = request.POST.get("word")
        cur = connection.cursor()
        cur.execute(
            'SELECT time,uid,username,text,like_count,following,followed FROM comment')
        selected = cur.fetchall()
        comment_list = []
        for item in selected:
            comment_list.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        cur.execute(
            'SELECT id FROM comment')
        selected2 = cur.fetchall()
        id = None
        for item in selected2:
            id = item[0]
        # if request.method == "GET":
        #     return render(request, "sensitivity.html")
        # elif request.method == "POST":
        #     sen = request.POST.get("word")
        #     # return render(request,"popup_response.html",{"sen":sen})
        cur.execute('DROP TABLE sensitivity')
        sensitive = []
        sensitive.append(sen)
        match_sensitive.main(sensitive, 'comment', 'uid')
        cur.execute('SELECT id FROM sensitivity')
        sensitive_id = cur.fetchall()
        mailbody = ''
        for item in sensitive_id:
            mailbody += item[0].__str__() + '\n'
        sendmail('1170301026@stu.hit.edu.cn', '敏感内容id', mailbody)
        for c in comment_list:
            uid = c[1]
            for item in sensitive_id:
                if uid == item[0]:
                    comment_list.remove(c)
        context = {
            'wid': id,
            'comment_list': comment_list,
        }
        return render(request, "comment_results.html", context)


def wordcloud(request):
    cur = connection.cursor()
    cur.execute(
        'SELECT id FROM comment')
    selected = cur.fetchall()
    id = None
    for item in selected:
        id = item[0]
    """读取图片"""
    filename = id + ".png"
    imagepath = os.path.join(settings.BASE_DIR, "weibo_crawler/weibo_results/comment/{}".format(filename))
    with open(imagepath, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")


def topic_filter(request):
    if request.method == "GET":
        return render(request, "sensitivity.html")
    elif request.method == "POST":
        sen = request.POST.get("word")
        cur = connection.cursor()
        cur.execute(
            'SELECT user_id, screen_name,text, created_at, attitudes_count, comments_count,reposts_count FROM topic')
        selected = cur.fetchall()
        topic_list = []
        for item in selected:
            topic_list.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        cur.execute('DROP TABLE sensitivity')
        sensitive = []
        sensitive.append(sen)
        match_sensitive.main(sensitive, 'topic', 'user_id')
        cur.execute('SELECT id FROM sensitivity')
        sensitive_id = cur.fetchall()
        mailbody = ''
        for item in sensitive_id:
            mailbody += item[0].__str__() + '\n'
        sendmail('1170301026@stu.hit.edu.cn', '敏感内容id', mailbody)
        for c in topic_list:
            uid = c[0]
            for item in sensitive_id:
                if uid == item[0]:
                    topic_list.remove(c)
        context = {
            'topic_list': topic_list,
        }
        return render(request, "topic_results.html", context)
