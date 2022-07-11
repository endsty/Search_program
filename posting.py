import os
import re
import pandas as pd
import operator


def stop_word():
    stopwords = []
    with open('stopword.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for i in f.readlines():
            stopwords.append(i.rstrip())
    return stopwords


def read_file(stopwords):
    root_dir = r'C:\Users\HERX\Desktop\代码\python\智能检索\已分词数据'
    dir_list = []
    ls = os.listdir(root_dir)
    for i in range(0, len(ls)):
        path = os.path.join(root_dir, ls[i])
        if os.path.isfile(path):
            dir_list.append(path)
    file_count = 0
    dir_dict = {}
    for path in dir_list:
        file_count += 1
        with open(path, 'r', encoding='GBK', errors='ignore') as f:
            read = f.read()
            text_tokens = re.findall(r'[\u4e00-\u9fa5]+', read)
            text_tokens = list(text_tokens)
            tokens_without_sw = []
            for word in text_tokens:        # 删除停用词
                if word not in stopwords:
                    tokens_without_sw.append(word)
            for item in tokens_without_sw:
                if item not in dir_dict.keys():
                    dir_dict[item] = {}
                    dir_dict[item].update({'df': 0})
                if item in dir_dict.keys():
                    if file_count not in dir_dict[item].keys():
                        dir_dict[item][file_count] = 1
                    else:
                        dir_dict[item][file_count] += 1
            print('managed file:', file_count)
    for item in dir_dict.keys():
        dir_dict[item]['df'] = len(list(dir_dict[item].keys())) - 1
    dir_dict = sorted(dir_dict.items(), key=operator.itemgetter(0))

    return dir_dict


def main():
    stopwords = stop_word()
    dict_ = read_file(stopwords)
    df = pd.DataFrame(dict_)
    df.to_csv(path_or_buf='dir_dict.csv', encoding='utf8')
    print(df)


if __name__ == '__main__':
    main()
