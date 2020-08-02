import jieba

txt = open("2018-3.txt", encoding="utf-8").read()  # 'wuxi.txt' 更换你的文件（txt格式）


def jiebafenci(txt, wordslist):
    jieba.load_userdict('tingcibiao.txt')
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    lst = []
    for i in range(len(wordslist)):
        try:
            print(wordslist[i], counts[wordslist[i]])
        except:
            lst.append(wordslist[i])
    print('不存在的词:', lst)


if __name__ == '__main__':
    txt = open("2020-7.txt", encoding="utf-8").read()  # 'wuxi.txt' 更换你的文件（txt格式）
    need_words = open("tingcibiao.txt", encoding="utf-8").read()  # 这个是要查找的词的txt文件 每个词一行
    find = need_words.split()
    jiebafenci(txt, find)

