import os
import csv
import ast


def get_dict(key):
    """
    获取关键词字典
    :return:key:{???}
    """
    os.getcwd()
    user_dict = {}
    with open('dir_dict.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['0'] == key:
                user_dict = ast.literal_eval(row['1'])
                break
    return user_dict


def get_textlist():
    """
    获取分词数据名称列表
    :return: text_list[]
    """
    root_dir = r'C:\Users\HERX\Desktop\代码\python\智能检索\已分词数据'
    text_list = []
    ls = os.listdir(root_dir)
    for i in range(0, len(ls)):
        path = os.path.join(root_dir, ls[i])
        if os.path.isfile(path):
            text_list.append(ls[i])
    return text_list


def and_boole(key1_dict, key2_dict):
    """
    进行and布尔运算
    :param key1_dict:
    :param key2_dict:
    :return: 关于key1与key2 and合并后的字典
    """
    new_dict = {}
    if key1_dict['df'] <= key2_dict['df']:
        for i in key1_dict.keys():
            if i in key2_dict.keys():
                new_dict[i] = key1_dict[i] + key2_dict[i]
    else:
        for i in key2_dict.keys():
            if i in key1_dict.keys():
                new_dict[i] = key1_dict[i] + key2_dict[i]
    new_dict['df'] = len(list(new_dict.keys())) - 1
    return new_dict


def or_boole(key1_dict, key2_dict):
    """
    进行or布尔运算
    :param key1_dict:
    :param key2_dict:
    :return: 关于key1与key2 or合并后的字典
    """
    new_dict = {'df': 0}
    for i in range(1, 533):  # 一共532个文件
        if i not in key1_dict.keys() and i in key2_dict.keys():
            new_dict[i] = key2_dict[i]
        if i not in key2_dict.keys() and i in key1_dict.keys():
            new_dict[i] = key1_dict[i]
        if i in key2_dict.keys() and i in key1_dict.keys():
            new_dict[i] = key1_dict[i] + key2_dict[i]
    new_dict['df'] = len(list(new_dict.keys())) - 1
    print(new_dict)
    return new_dict


def not_boole(key_dict):
    """
    进行not布尔运算
    :param key_dict:
    :return:
    """
    new_dict = {'df': 0}
    for i in range(1, 533):  # 一共532个文件
        if i not in key_dict.keys():
            new_dict[i] = 0
    new_dict['df'] = len(list(new_dict.keys())) - 1
    return new_dict


def boole_sort(last_dict):
    """
    对Boole查询后的文件按照tf进行排序
    :param last_dict:布尔查询后返回的字典集
    :return:NONE
    """
    text = []
    if not last_dict:
        return text
    text_list = get_textlist()
    last_dict.pop('df')
    dir_list = sorted(last_dict.items(), key=lambda i: i[1])
    for i, j in dir_list:
        text.append(text_list[i - 1])
    return text


def remake_information(string):
    """
    对收集到的信息进行处理
    :param string: 查询信息
    :return:
    """
    # 以空格为界限划分开来
    key_list = string.split()    # 规定按’ ‘分割符号
    print(key_list)
    key_dit = {}
    last_dit = {}
    if len(key_list) == 1:
        key_dit = get_dict(key_list[0])
        text_list = boole_sort(key_dit)
    else:
        for i in range(len(key_list)):
            if key_list[i] == 'not':
                key_dit[key_list[i + 1]] = get_dict(key_list[i+1])
                last_dit = not_boole(key_dit[key_list[i + 1]])
                key_dit[key_list[i + 1]] = last_dit
        while 'not' in key_list:
            key_list.remove('not')
        for i in range(0, len(key_list), 2):
            if key_list[i] not in key_dit.keys():
                key_dit[key_list[i]] = get_dict(key_list[i])
        for i in range(1, len(key_list), 2):
            if key_list[i] == 'and':
                last_dit = and_boole(key_dit[key_list[i - 1]], key_dit[key_list[i + 1]])
                key_dit[key_list[i + 1]] = last_dit
            if key_list[i] == 'or':
                last_dit = or_boole(key_dit[key_list[i - 1]], key_dit[key_list[i + 1]])
                print(key_dit[key_list[i - 1]], key_dit[key_list[i + 1]])
                key_dit[key_list[i + 1]] = last_dit
        text_list = boole_sort(last_dit)
    print(len(text_list))
    return text_list
