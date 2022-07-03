# -*- coding: utf-8 -*-
# @Author : wangyanrong
# @Email  : 408492397@qq.com
# @Date   : 2022/5/11 15:14
import os.path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

news_type = 'sina_jiaoyu'
url = 'http://www.worldwidewords.org/genindex.htm'
class_name = '.contentcol'


def get_text(href):
    res = requests.get(href)  # 模拟get
    # 请求获取链接返回的内容
    res.encoding = 'utf-8'  # 设置编码格式为utf-8
    soup = BeautifulSoup(res.text, 'html.parser')
    p_list = soup.select('.contentcol')[0].select('p')
    text = [p.text for p in p_list if 'Pronounced' not in p.text]
    return '\n'.join(text)


if __name__ == '__main__':
    res = requests.get(url)  # 模拟get
    # 请求获取链接返回的内容
    res.encoding = 'utf-8'  # 设置编码格式为utf-8
    soup = BeautifulSoup(res.text, 'html.parser')  # 前⾯已经介绍将html⽂档格式化为⼀个树形结构，每个节点都是⼀个对python对象，⽅便获取节点内容
    news_href_list = []
    text = ''
    check_point = 2402

    file_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(file_path, os.path.join('news', '万维词汇网.txt'))
    if not os.path.exists(filename):
        f = open(filename, 'w', encoding="utf-8")
        f.close()
    for news in soup.select(class_name):
        for a in news.select('a'):
            news_href_list.append('http://www.worldwidewords.org/' + a['href'])

    for href in tqdm(news_href_list[check_point:], '语料爬取中'):
        text = get_text(href) + '\n\n'
        with open(filename, 'a', encoding="utf-8") as f:
            f.write(text)
