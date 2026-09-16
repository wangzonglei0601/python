"""选择新浪新闻国内频道作为目标网站：https://news.sina.com.cn/china/
爬取首页的前10条新闻标题和发布时间。
把数据保存为news.csv文件，字段不少于两列。"""
import requests
import json
import csv

from urllib3.contrib.emscripten import fetch


class html(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "Cookie": "NowDate = FriAug07202602: 30:27GMT + 0800"
        }
        self.url = 'https://news.sina.com.cn/china/'
    def fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"{e}问题")
    def parser(self, html):
        if not html:
            return None

        print(html)

        return None
html = html()
html.parser(fetch)