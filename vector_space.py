import boole_search
import math
import time

# 文档集中文档的个数 N
N = 532


def tf_idf(key_list):
    """
    构建权重矩阵
    :param key_list: 需要查询的关键词表
    :return:关键词的权重矩阵和query的tf_idf
    """
    # key_list的字典集
    dir_dict = {}
    text_map = {}
    start = time.time()
    for key in key_list:
        dir_dict[key] = boole_search.get_dict(key)
    # 对关键词进行and运算
    end = time.time()
    print('程序调用dir_dict时间为：', (end - start), 's')
    last_ = dir_dict[key_list[0]]
    for i in range(1, len(key_list)):
        last_ = boole_search.and_boole(last_, dir_dict[key_list[i]])
    for key in dir_dict.keys():
        idf = float(math.log(N / dir_dict[key]['df'], 10))
        for i in dir_dict[key].keys():
            if i != 'df':
                if i in last_.keys():
                    w = float(1 + math.log(dir_dict[key][i], 10))*idf
                    if i not in text_map.keys():
                        text_map[i] = w
                    elif i in text_map.keys():
                        text_map[i] = text_map[i] + w
    return text_map


def vector_space(text_map):
    """
    计算排序式检索的向量空间
    :param text_map:
    :return: 按照tf_idf排序的text_list
    """
    # sum(wqi*wdi)
    text_list = sorted(text_map.items(), key=lambda j: j[1], reverse=True)
    return text_list


def print_text(text_list):
    """
    print information
    :param text_list:
    :return:
    """
    text = []
    text_ = boole_search.get_textlist()
    num = 0
    for i, j in text_list:
        if j > 0:
            text.append(text_[i - 1])
            num = num+1
    print('返回文档数目：',num)
    return text


def start_search(string):
    """
    对收集到的信息进行处理
    :param string: 查询信息
    :return
    """
    key_list = string.split()
    print(key_list)
    dir_dit = tf_idf(key_list)
    text_list = vector_space(dir_dit)
    text = print_text(text_list)
    return text
