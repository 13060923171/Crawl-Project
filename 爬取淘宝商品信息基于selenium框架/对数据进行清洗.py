def clearBlankLine():
    file1 = open(input("请输入要清洗的文本(包括后缀):"), 'r',encoding="utf-8") # 要去掉空行的文件
    file2 = open('清洗好的文本.txt', 'w', encoding='utf-8') # 生成没有空行的文件
    try:
        for line in file1.readlines():
            line = line.replace("'","").replace('"',"").replace('[','').replace(']','').replace(",)","").replace("(","")
            file2.write(line)
    finally:
        file1.close()
        file2.close()


if __name__ == '__main__':
    clearBlankLine()
