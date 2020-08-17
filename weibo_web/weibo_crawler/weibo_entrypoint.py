# coding:utf-8
import signal
import time

import subprocess
from scrapy import cmdline
# from scrapy.crawler import CrawlerProcess
import os
import stat
import shutil


# command: scrapy crawl search -s JOBDIR=crawls/search
# cmdline.execute(['scrapy', 'crawl', 'search', '-s', 'JOBDIR=crawls/search'])
# from scrapy.utils.project import get_project_settings

# filePath:文件夹路径
def delete_file(filePath):
    if os.path.exists(filePath):
        for fileList in os.walk(filePath):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree(filePath)
        return "delete ok"
    else:
        return "no filepath"


if __name__ == "__main__":
    # if os.path.exists("crawls/search"):
    #     delete_file("crawls/search")
    # cmdline.execute(['scrapy', 'crawl', 'search', '-s', 'JOBDIR=crawls/search'])

    process = subprocess.Popen("scrapy crawl search -s JOBDIR=crawls/search", shell=True)
    pid = process.pid
    time.sleep(300)
    os.kill(pid, signal.CTRL_C_EVENT)
