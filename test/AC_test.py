import ahocorasick
A = ahocorasick.Automaton()

# 向trie树中添加单词
for index,word in enumerate("he her hers she".split()):
    A.add_word(word, (index, word))
# 用法分析add_word(word,[value]) => bool
# 根据Automaton构造函数的参数store设置，value这样考虑：
# 1. 如果store设置为STORE_LENGTH，不能传递value，默认保存len(word)
# 2. 如果store设置为STORE_INTS，value可选，但必须是int类型，默认是len(automaton)
# 3. 如果store设置为STORE_ANY，value必须写，可以是任意类型

# 测试单词是否在树中
if "he" in A:
    print(True)
else:
    print(False)


print(A.get("he"))
# (0,'he')
print(A.get("cat","<not exists>"))
# '<not exists>'
print(A.get("dog"))
# KeyError

# 将trie树转化为Aho-Corasick自动机
A.make_automaton()

# 找到所有匹配字符串
for item in A.iter("_hershe_"):
    print(item)
#(2,(0,'he'))
#(3,(1,'her'))
#(4, (2, 'hers'))
#(6, (3, 'she'))
#(6, (0, 'he'))