import ahocorasick
import functools
import abc

# import sys
# import pymysql
# import traceback
#
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header


class ReRule(metaclass=abc.ABCMeta):
    def __init__(self):
        self.children = []

    @property
    def sat(self):
        return True

    def has_child(self):
        return bool(self.children)

    def simplify_children(self):
        if not self.has_child():
            return []
        return list(map(lambda child: child.simplify(), self.children))

    def simplify(self):
        return self


class Contain(ReRule):
    def __init__(self, word, cond=None):
        if not word:
            raise Exception("Zero-length word is invalid")
        self.word = word
        self.count = 0
        self.cond = cond
        self.children = []

    @property
    def sat(self):
        if self.cond:
            return self.cond(self.count)
        else:
            return bool(self.count)

    def initialize(self):
        self.count = 0

    def process(self):
        self.count += 1


class Or(ReRule):
    def __init__(self, *rules):
        self.children = list(rules)

    @property
    def sat(self):
        for child in self.children:
            if child.sat:
                return True
        return False

    def simplify(self):
        children = self.simplify_children()
        new_children = []
        for child in children:
            if isinstance(child, Or):
                new_children.extend(child.children)
            else:
                new_children.append(child)
        return Or(*new_children)


class And(ReRule):
    def __init__(self, *rules):
        self.children = list(rules)
        self.value = 0

    @property
    def sat(self):
        return functools.reduce(lambda y, x: x.sat and y, self.children, True)

    def simplify(self):
        children = self.simplify_children()
        new_rules = []
        for child in children:
            if isinstance(child, And):
                new_rules += child.children
            else:
                new_rules.append(child)
        return And(*new_rules)


class ReAutomaton(object):

    def __init__(self):
        self.automaton = ahocorasick.Automaton()
        self.rule = None
        self.word_rule = {}

    def set_rule(self, rule):
        self.rule = rule
        # simplify rule
        self.rule = self.rule.simplify()
        self.compile()

    def compile(self):
        if not self.rule:
            return
        self.word_rule = {}
        if not isinstance(self.rule, Contain):
            stack = [self.rule]
            while stack:
                rule = stack.pop()
                children = rule.children
                for idx, child_rule in enumerate(children):
                    if isinstance(child_rule, Contain):
                        existed_rule = self.word_rule.get(child_rule.word)
                        if existed_rule:
                            children[idx] = existed_rule
                        else:
                            self.word_rule[child_rule.word] = child_rule
                    else:
                        stack.append(child_rule)
        else:
            self.word_rule[self.rule.word] = self.rule
        self.automaton.clear()
        for rule in self.word_rule.values():
            word = rule.word
            self.automaton.add_word(word, word)
        self.automaton.make_automaton()

    def match(self, haystack):
        if not self.rule:
            return False
        for rule in self.word_rule.values():
            rule.initialize()
        for _, word in self.automaton.iter(haystack):
            contain_rule = self.word_rule.get(word)
            assert contain_rule
            contain_rule.process()
        return self.rule.sat


def test_1():
    a = Contain("love")
    b = Contain("death")
    c = Contain("robot")
    d = Contain("fuck")
    ab = And(a, b)
    cd = And(c, d)
    abcd = Or(ab, cd)
    rea = ReAutomaton()
    rea.set_rule(abcd)
    print(rea.match("lov love robo death"))
    print(rea.match("fuc robot deat fuck"))
    print(rea.match("dea love robo robot"))
    print(rea.match("lov death robo fuck"))

def test_2():
    a = Contain("中国小说网")
    b = Contain("小说网站")
    c = Contain("各种小说")
    d = Contain("网站")
    ab = And(a, b)
    cd = And(c, d)
    abcd = Or(ab, cd)
    rea = ReAutomaton()
    rea.set_rule(abcd)
    print(rea.match("中国小说网是一个各种小说都有的小说网站，小说网有个类小说作家"))

if __name__ == "__main__":
    test_1()
    test_2()
    # db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='zhihu_spider')
    # cursor = db.cursor()
    # # print(str(len(sys.argv)))
    # # print(sys.argv[1])
    # if (len(sys.argv) == 3):
    #     # print(sys.argv[1])
    #     # print(sys.argv[2])
    #     sql = 'select * from answer where id=' + sys.argv[2]
    #     # print(sql)
    #     try:
    #         cursor.execute(sql)
    #         one = cursor.fetchone()
    #         if (one):
    #             title = one[2]
    #             content = one[5]
    #             rule = eval(sys.argv[1])
    #             rea = ReAutomaton()
    #             rea.set_rule(rule)
    #             print(rea.match(title) or rea.match(content))
    #     except:
    #         print(traceback.format_exc())
    #         print('Error')
    # else:
    #     sql = 'select * from answer'
    #     try:
    #         cursor.execute(sql)
    #         one = cursor.fetchone()
    #         reportList = []
    #         while (one):
    #             title = one[2]
    #             url = one[1]
    #             content = one[5]
    #             rule = eval(sys.argv[1])
    #             rea = ReAutomaton()
    #             rea.set_rule(rule)
    #             if (rea.match(title) or rea.match(content)):
    #                 reportList.append(url)
    #                 # print(url)
    #                 # print(str(len(reportList)))
    #             one = cursor.fetchone()
    #         if (len(reportList) != 0):
    #             username = '18846073585@163.com'
    #             password = 'fendou1314'
    #             receiver = '1605936835@qq.com'
    #             subject = '违规网页列表'
    #             text = "\n".join(reportList)
    #             # print(text)
    #             msg = MIMEText(text, 'plain', 'utf-8')
    #             msg['Subject'] = subject
    #             msg['From'] = '18846073585@163.com <18846073585@163.com>'
    #             msg['To'] = '1605936835@qq.com'
    #             smtp = smtplib.SMTP()
    #             smtp.connect('smtp.163.com')
    #             smtp.set_debuglevel(1)
    #             smtp.login(username, 'fendou1314')
    #             smtp.sendmail(username, receiver, msg.as_string())
    #             smtp.quit()
    #
    #     except:
    #         print(traceback.format_exc())
    #         print('Error')
