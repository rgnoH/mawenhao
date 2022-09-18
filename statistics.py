import os
import jieba
import csv
from matplotlib import pyplot as plt
from tqdm import tqdm as tq

statfile_path = './stat/'
datafile_path = './data/'
names = ["北京规划自然资源", "城市更新网URN", "城市规划学刊upforum", "城事会客厅", "清华同衡规划播报", 
         "新土地规划人", "住房与社区规划学委会", "cityif", "THU社区规划"]
keywords = ["责师", "责任双师", "责任规划师"]
header = ["词语", "词频", "出现文章占比"]

'''
统计的信息：
先统计出每个词的出现次数（不同公众号分别统计+总计），排好序保存到csv文件里
出现关键词的文章数和比例（不同公众号分别统计+总计）
后续再考虑画图/进一步根据需求来分析
'''

def inc_dict(dict, key):
    if key in dict.keys():
        dict[key] += 1
    else:
        dict[key] = 1

# 加载用户词典（包含所有 keywords）
jieba.load_userdict('keywordsdict.txt')
# 设定停用词表，过滤掉常用但不重要的词语和标点符号
with open('stopwords.txt', 'r', encoding='utf-8') as f:
    # stopwords source:  https://www.cnblogs.com/mfmdaoyou/p/6848772.html
    stopwords = f.read().strip().split('\n')

all_dict_appear = {}
all_dict_cnt = {}
n_files = 0

for name in tq(names): # 枚举每个公众号
    dict_appear = {} # 
    dict_cnt = {} # 该公众号内，每个词出现的总次数
    files = os.listdir(datafile_path + name + '/texts')
    n_files += len(files)
    for file in tq(files): # 枚举每个文章
        with open(datafile_path + name + '/texts/' + file, 'r', encoding='utf-8') as f:
            text = f.read()
        word_list = jieba.cut(text)
        is_appear = {}
        for word in word_list:
            if word in stopwords:
                continue
            inc_dict(all_dict_cnt, word)
            inc_dict(dict_cnt, word) # 统计出现次数
            is_appear[word] = 1
        for word in is_appear.keys():
            inc_dict(all_dict_appear, word)
            inc_dict(dict_appear, word)
    with open(statfile_path + name + '.csv', 'w', encoding='utf-8', newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerow(header)
        cnt_sorted = sorted(dict_cnt.items(), key=lambda x: x[1], reverse=True)[:5000]
        for word, cnt in cnt_sorted:
            f_writer.writerow([word, cnt, dict_appear[word] / len(files)])

with open(statfile_path + 'all.csv', 'w', encoding='utf-8', newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerow(header)
        cnt_sorted = sorted(all_dict_cnt.items(), key=lambda x: x[1], reverse=True)[:5000]
        for word, cnt in cnt_sorted:
            f_writer.writerow([word, cnt, all_dict_appear[word] / n_files])