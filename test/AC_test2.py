import ahocorasick

A = ahocorasick.Automaton()

# 添加单词
for index,word in enumerate("cat catastropha rat rate bat".split()):
    A.add_word(word, (index, word))

# prefix
print(list(A.keys("cat")))
## ["cat","catastropha"]

print(list(A.keys("?at","?",ahocorasick.MATCH_EXACT_LENGTH)))
## ['bat','cat','rat']

print(list(A.keys("?at?", "?", ahocorasick.MATCH_AT_MOST_PREFIX)))
## ["bat", "cat", "rat", "rate"]

print(list(A.keys("?at?", "?", ahocorasick.MATCH_AT_LEAST_PREFIX)))
## ['rate']
## keys用法分析
## keys([prefix, [wildcard, [how]]]) => yield strings
## If prefix (a string) is given, then only words sharing this prefix are yielded.
## If wildcard (single character) is given, then prefix is treated as a simple pattern with selected wildcard. Optional parameter how controls which strings are matched:
## MATCH_EXACT_LENGTH [default]：Only strings with the same length as a pattern’s length are yielded. In other words, literally match a pattern.
## MATCH_AT_LEAST_PREFIX：Strings that have length greater or equal to a pattern’s length are yielded.
## MATCH_AT_MOST_PREFIX：Strings that have length less or equal to a pattern’s length are yielded.