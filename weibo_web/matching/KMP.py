class KMP:
    # 获取next数组
    def get_next(self, T):
        i = 0
        j = -1
        next_val = [-1] * len(T)
        while i < len(T)-1:
            if j == -1 or T[i] == T[j]:
                i += 1
                j += 1
                # next_val[i] = j
                if i < len(T) and T[i] != T[j]:
                    next_val[i] = j
                else:
                    next_val[i] = next_val[j]
            else:
                j = next_val[j]
        return next_val

    # KMP算法
    def kmp(self, S, T):
        i = 0
        j = 0
        next = self.get_next(T)
        while i < len(S) and j < len(T):
            if j == -1 or S[i] == T[j]:
                i += 1
                j += 1
            else:
                j = next[j]
        if j == len(T):
            return i - j
        else:
            return -1


if __name__ == '__main__':
    haystack = 'acabaabaabcacaabc'
    needle = 'abaabcac'

    k = KMP()
    print(k.kmp(haystack, needle))    # 输出 "5"

    n = '中国小说网'
    m = '中国小说网是一个各种小说都有的小说网站，小说网有个类小说作家'
    print(k.kmp(m, n))  # 输出 "0"