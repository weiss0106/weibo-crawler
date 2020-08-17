import datetime


def setup():
    for i in range(30000):
        file = open('ac_test/' + str(i) + '.txt', 'w')
        file.write('qw殷俊qqqwweq学习资源、王志青等wj 的置顶功能dahai,殷俊dahabekgwbnudaihai王志清殷殷俊')
        file.close()


# 结点类
class node:
    def __init__(self, ch):
        self.ch = ch  # 结点值
        self.fail = None  # Fail指针
        self.tail = 0  # 尾标志：标志为 i 表示第 i 个模式串串尾
        self.child = []  # 子结点
        self.childvalue = []  # 子结点的值


# AC自动机类
class acmation:
    def __init__(self):
        self.root = node("")  # 初始化根结点
        self.count = 0  # 模式串个数

    # 第一步：模式串建树
    def insert(self, strkey):
        self.count += 1  # 插入模式串，模式串数量加一
        p = self.root
        for i in strkey:
            if i not in p.childvalue:  # 若字符不存在，添加子结点
                child = node(i)
                p.child.append(child)
                p.childvalue.append(i)
                p = child
            else:  # 否则，转到子结点
                p = p.child[p.childvalue.index(i)]
        p.tail = self.count  # 修改尾标志

    # 第二步：修改Fail指针
    def ac_automation(self):
        queuelist = [self.root]  # 用列表代替队列
        while len(queuelist):  # BFS遍历字典树
            temp = queuelist[0]
            queuelist.remove(temp)  # 取出队首元素
            for i in temp.child:
                if temp == self.root:  # 根的子结点Fail指向根自己
                    i.fail = self.root
                else:
                    p = temp.fail  # 转到Fail指针
                    while p:
                        if i.ch in p.childvalue:  # 若结点值在该结点的子结点中，则将Fail指向该结点的对应子结点
                            i.fail = p.child[p.childvalue.index(i.ch)]
                            break
                        p = p.fail  # 否则，转到Fail指针继续回溯
                    if not p:  # 若p==None，表示当前结点值在之前都没出现过，则其Fail指向根结点
                        i.fail = self.root
                queuelist.append(i)  # 将当前结点的所有子结点加到队列中

    # 第三步：模式匹配
    def runkmp(self, strmode):
        p = self.root
        cnt = {}  # 使用字典记录成功匹配的状态
        for i in strmode:  # 遍历目标串
            while i not in p.childvalue and p is not self.root:
                p = p.fail
            if i in p.childvalue:  # 若找到匹配成功的字符结点，则指向那个结点，否则指向根结点
                p = p.child[p.childvalue.index(i)]
            else:
                p = self.root
            temp = p
            while temp is not self.root:
                if temp.tail:  # 尾标志为0不处理
                    if temp.tail not in cnt:
                        cnt.setdefault(temp.tail)
                        cnt[temp.tail] = 1
                    else:
                        cnt[temp.tail] += 1
                temp = temp.fail
        return cnt  # 返回匹配状态
        # 如果只需要知道是否匹配成功，则return bool(cnt)即可
        # 如果需要知道成功匹配的模式串种数，则return len(cnt)即可


def main():
    key = ["殷俊", "王志青", "dahai", "qww"]  # 创建模式串
    acp = acmation()

    for i in key:
        acp.insert(i)  # 添加模式串

    acp.ac_automation()

    start = datetime.datetime.now()  # 开始时间
    for i in range(10000):
        file = open(r'ac_test/' + str(i) + '.txt', 'r')
        text = ''
        while True:
            row = file.readline()  # 读每一行
            if not row:  # 如果全部读完
                break  # 就跳出
            text = text + row
        d = acp.runkmp(text)  # 运行自动机
    '''.
        print (d)                               #打印
        for i in d.keys():
            print(key[i-1],d[i])                #将子串匹配的数量显示
    '''
    end = datetime.datetime.now()  # 结束时的时间
    print('总共花费时间是:', end - start)  # 打印出总共花费时间


if __name__ == '__main__':
    setup()
    main()
