import csv

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import json


class Spider(object):
    def __init__(self, start_url, item_selector, fields, next_selector=None):
        self.start_url = start_url
        self.item_selector = item_selector
        self.fields = fields
        self.next_selector = next_selector
        self.data = []
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def fetch(self,url):
        try:
            response=requests.get(self.start_url, headers=self.headers, timeout=5)
            response.encoding="utf-8"
            response.raise_for_status()
            print("网页正常200")
            # BeautifulSoup(response.text,"html.parser")
            return BeautifulSoup(response.text,"html.parser")
        except Exception as e:
            print("{e}错误")
            return None
    def parse(self,soup):
        items=soup.select(self.item_selector)
        if not(items):
            print("没有元素{self.itme_selector}错误")
        for item in items:
            row = {}
            for field in self.fields:
                selector=field["selector"]
                attr=field["attr"]
                element = item.select_one(selector)
                if element:
                    if attr == "text":
                        value = element.get_text(strip=True)
                    else:
                        value = element.get(attr ,"")
                else:
                    value = ""
                print(value)
                attr = field.get("attr","text")
                eitem=item.select_one(selector)
                if eitem:
                    if attr == "text":
                        value = eitem.get_text(strip=True)
                    else:
                        value = eitem.get(attr,"")
                else:
                    value = ""
                row[field["name"]]=value
            self.data.append(row)
        print(f"以解析{len(items)}当前共{self.data}条数据")

    def next_page(self,soup):
        if not self.start_url:
            return None
        next_link = soup.select_one(self.next_selector)
        if next_link and next_link.get("href"):
            return urljoin(self.start_url, next_link.get("href"))
        return None

    def save(self,filename = "result.csv"):
        if not self.data:
            return None
        with open(filename, "w",newline="", encoding="utf-8") as f:
            filenames=[field["name"]for field in self.fields]
            json.dump(self.data,f,ensure_ascii=False,indent=4,sort_keys=True,separators=(",",":"))
            # writer = csv.DictWriter(f,fieldnames=filenames)
            # writer.writeheader()
            # writer.writerows(self.data)
        print(f"已保存{len(self.data)},数据，到{filename}文件")
        return None

    def run(self,max_pages=None):
        url = self.start_url
        page =1
        while url:
            print(f"爬取第{page}页{url}")
            soup = self.fetch(url)
            if soup:
                self.parse(soup)
                url = self.next_page(soup)
                page+=1
                time.sleep(1)
                if max_pages and page > max_pages:
                    print(f"已到达最大页数{max_pages}")
                    break
            else:
                break
        self.save()
if __name__ == '__main__':
    # ==================== 使用示例 ====================
    pass
if __name__ == "__main__":
    # 示例1：爬取 books.toscrape.com 的书籍信息（有分页）
    spider1 = Spider(
        start_url="https://books.toscrape.com/catalogue/page-1.html",
        item_selector = ".product_pod",
        fields =[
            {"selector":"h3 a",
            "name":"书名",
             "attr":"title"},

            {"name":"价格", "selector":".price_color","attr":"text"}],
        next_selector = ".next a"
    )
    spider1.run(max_pages=1)

    # 示例2：爬取百度热搜（无分页，一次性页面）
    # spider2 = Spider(
    #     start_url="https://top.baidu.com/board?tab=realtime",
    #     item_selector=".category-wrap_iQLoo",
    #     fields=[
    #         {"name": "标题", "selector": ".c-single-text-ellipsis", "attr": "text"},
    #         {"name": "热度", "selector": ".hot-index_1Bl1a", "attr": "text"}
    #     ],
    #     next_selector=None  # 没有下一页
    # )
    # # spider2.run()
