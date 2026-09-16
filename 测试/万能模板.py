from urllib.parse import urljoin

import requests
import json
from bs4 import BeautifulSoup
import time



class Spider(object):
    def __init__(self,start_url,item_selector,fields,next_selector=None):
        self.start_url = start_url
        self.item_selector = item_selector
        self.fields = fields
        self.next_selector = next_selector
        self.data = []
        self.headers = {"User-Agent":"Mozilla/5.0"}

    #请求
    def fetch(self):
        try:
            response=requests.get(self.start_url,headers=self.headers,timeout=5)
            response.encoding="utf-8"
            response.raise_for_status()
            print("网页正常200")
            return BeautifulSoup(response.text,"html.parser")
        except Exception as e:
            print(f"{e}错误")
    #解析
    def parse(self,soup):
        items=soup.select(self.item_selector)
        if not items:
            print("元素是空的{}".format(self.item_selector))
            return None
        for item in items:
            row = {}
            for field in self.fields:
                selector=field["selector"]
                attr = field["attr"]
                element = item.select_one(selector)
                if element:
                    if attr == "text":
                        value = element.get_text(strip=True)
                    else:
                        value = element.get(attr,"空")
                else:
                    value = "空"
                print(value)
                row[field["name"] ]= value
            self.data.append(row)
        print(f"以解析{len(items)}数据，共{self.data}条")
        return None
    #下一页
    def next_page(self,soup):
        if not self.start_url:
            return None
        nextlink = soup.select_one(self.next_selector)
        if nextlink and nextlink.get("href"):
            return urljoin(self.start_url,nextlink.get("href"))

        return None
    #保存
    def vase(self,filename = "resu.csv"):
        if not self.data:
            return None
        with open(filename,"w",newline="",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
            print("已保存到{}数据到{}".format(self.data,filename))

        return None

    #允许
    def run(self,max_pages):
        url = self.start_url
        page = 1
        while url:
            print("爬取第一个{page}".format(page=page))
            soup = self.fetch()
            if soup:
                self.parse(soup)
                url = self.next_page(soup)
                page += 1
                time.sleep(1)
                if max_pages and page > max_pages:
                    break
            else:
                break
if __name__ == "__main__":
    spider1 = Spider(
        start_url="https://books.toscrape.com/catalogue/page-1.html",
        item_selector=".product_pod",
        fields=[
            {"selector": "h3 a",
             "name": "书名",
             "attr": "title"},

            {"name": "价格", "selector": ".price_color", "attr": "text"}],
        next_selector=".next a"
    )
    spider1.run(max_pages=1)



