
class BF:
    def bf(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: int
        """
        i = 0
        j = 0
        while i < len(S) and j < len(T):
            if S[i] == T[j]:    # 依次比较，相等则比较下一个字符
                i += 1
                j += 1
            else:    # 如果不相等，指针i需要回溯到上个起点的下一个位置
                     # 并从头开始比较
                i -= j - 1
                j = 0
        # while循环结束后，要么是找到合适匹配了，要么是遍历完主串都没有找到合适匹配
        if j == len(T):
            return i - j
        else:
            return -1

if __name__ == '__main__':
    haystack = 'acabaabaabcacaabc'
    needle = 'abaabcac'

    b = BF()
    print(b.bf(haystack, needle))    # 输出 "5"
    n = '中国小说网'
    m = '中国小说网是一个各种小说都有的小说网站，小说网有个类小说作家'
    print(b.bf(m, n))  # 输出 "0"
