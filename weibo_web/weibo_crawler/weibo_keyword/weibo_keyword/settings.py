# -*- coding: utf-8 -*-

BOT_NAME = 'weibo_keyword'
SPIDER_MODULES = ['weibo_keyword.spiders']
NEWSPIDER_MODULE = 'weibo_keyword.spiders'
COOKIES_ENABLED = False
LOG_LEVEL = 'ERROR'
# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'ALF=1592475078; SCF=ArHI5GnyVVVZPduX1hkZ2sh-7JYvOzRb6A6PKY1oT9HYGLCXZtr_kbO0Z1m9rRk_ZfiqgJ0TY7Sx04wrCi4IOIw.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWksjWGNNPVOAJP0r0VVrjL5JpX5KMhUgL.FoMXSKM0Sh.pSKB2dJLoIEXLxK-LBo5L12qLxK-L12qLB-qLxKML1hnLBo2LxK.L1KnLB.qLxKqLBoBL1-zt; SUB=_2A25zx8CBDeRhGeFK7lUS9CfNzjiIHXVRS-DJrDV6PUJbkdANLXXakW1NQyjFTYSkY8rCCdikEbN1rFcjPjaFELoP; SUHB=0HThijoCLD1jBB; SSOLoginState=1589883089; _T_WM=55060150345; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174'
}
ITEM_PIPELINES = {
    'weibo_keyword.pipelines.DuplicatesPipeline': 300,
    'weibo_keyword.pipelines.CsvPipeline': 301,
    'weibo_keyword.pipelines.MysqlPipeline': 302
    # 'weibo.pipelines.MongoPipeline': 303,
    # 'weibo.pipelines.MyImagesPipeline': 304,
    # 'weibo.pipelines.MyVideoPipeline': 305
}
# 要搜索的关键词列表，可写多个
KEYWORD_LIST = ['哈工大']
# 要搜索的微博类型，0代表搜索全部微博，1代表搜索全部原创微博，2代表热门微博，3代表关注人微博，4代表认证用户微博，5代表媒体微博，6代表观点微博
WEIBO_TYPE = 1
# 筛选结果微博中必需包含的内容，0代表不筛选，获取全部微博，1代表搜索包含图片的微博，2代表包含视频的微博，3代表包含音乐的微博，4代表包含短链接的微博
CONTAIN_TYPE = 0
# 筛选微博的发布地区，精确到省或直辖市，值不应包含“省”或“市”等字，如想筛选北京市的微博请用“北京”而不是“北京市”，想要筛选安徽省的微博请用“安徽”而不是“安徽省”，可以写多个地区，
# 具体支持的地名见region.py文件，注意只支持省或直辖市的名字，省下面的市名及直辖市下面的区县名不支持，不筛选请用”全部“
REGION = ['全部']
# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2020-06-13'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2020-06-13'
# 图片文件存储路径
IMAGES_STORE = './'
# 视频文件存储路径
FILES_STORE = './'
# 配置MongoDB数据库
# MONGO_URI = 'localhost'
# 配置MySQL数据库，以下为默认配置，可以根据实际情况更改，程序会自动生成一个名为weibo的数据库，如果想换其它名字请更改MYSQL_DATABASE值
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'lab'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'weibo'
