import re
import os
import requests
from lxml import etree
import time
import random
from tqdm import tqdm as tq

tasks = []
dir_path = './data/THU社区规划/'

def extract_html_from_jsons():
    filenames = os.listdir(dir_path + 'jsons')
    already_exist = set()
    f = open(dir_path + 'htmls.txt', 'r', encoding='utf-8')
    st_num = 0
    for line in f.readlines():
        num, url = line.strip().split()
        st_num = max(st_num, int(num) + 1)
        already_exist.add(url)
    f.close()
    print(f'{len(already_exist)} htmls already exists')
    new_html = []
    pattern = re.compile(r'"(http://mp.weixin.qq.com.*?)"')
    for file in filenames:
        g = open(dir_path + 'jsons/' + file, 'r', encoding='utf-8')
        htmls = pattern.findall(g.read())
        if len(htmls) == 0:
            print(file)
        for html in htmls:
            if html not in already_exist:
                new_html.append(html)
        g.close()
    f = open(dir_path + 'htmls.txt', 'a', encoding='utf-8')
    for i in range(len(new_html)):
        f.write(str(st_num + i) + ' ' + new_html[i] + '\n')
    f.close()
    print(f'{len(new_html)} htmls added, {len(new_html) + len(already_exist)} in total')

def extract_html_to_crawl():
    global tasks
    f = open(dir_path + 'htmls.txt', 'r', encoding='utf-8')
    all_htmls = set()
    for line in f.readlines():
        if len(line.strip()) > 0:
            num, url = line.strip().split()
            all_htmls.add((num, url))
    f.close()
    crawled_htmls = set()
    f = open(dir_path + 'htmls_crawled.txt', 'r', encoding='utf-8')
    for line in f.readlines():
        if len(line.strip()) > 0:
            num, url = line.strip().split()
            crawled_htmls.add((num, url))
    f.close()
    tasks = list(all_htmls - crawled_htmls)
    tasks.sort(key=lambda x : int(x[0]))

def crawl():
    err = open(dir_path + 'err_htmls.txt', 'a', encoding='utf-8')
    cnt = 0
    stp = 50 + random.randint(0,10)
    for num, url in tq(tasks):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        req = requests.get(url, headers = headers)
        if req.status_code == 200:
            tree = etree.HTML(req.text)
            title = tree.xpath('//h1/text()')
            content = [line for line in tree.xpath('//p//text()') if line.strip() != '']
            if len(title) == 1:
                with open(dir_path + 'htmls/' + num + '.html', 'w', encoding='utf-8') as f:
                    f.write(req.text)
                with open(dir_path + 'texts/' + num + '.txt', 'w', encoding='utf-8') as f:
                    f.write('标题: ' + title[0].strip() + '\n')
                    f.write('\n'.join(content))
                with open(dir_path + 'htmls_crawled.txt', 'a', encoding='utf-8') as f:
                    f.write(num + ' ' + url + '\n')
        else:
            err.write(f'[ERROR] status {req.status_code} at {url}')
        time.sleep(2 + random.random() * 2)
        cnt += 1
        if cnt == stp:
            stp += 50 + random.randint(0, 10)
            time.sleep(60 + 30 * random.random())
    err.close()


def main():
    extract_html_from_jsons()
    extract_html_to_crawl()
    crawl()

if __name__ == "__main__":
    main()