"""第一优先级：自动翻页与参数化
□ 在 __init__ 中接收 start_page 和 end_page 作为参数
□ 在 run 方法中循环请求每一页
□ 用 time.sleep(0.5) 控制请求间隔
□ 用命令行参数（sys.argv）接收起始页和结束页
第二优先级：异常处理与稳定性
□ 在 fetch_page 中加入 try-except，捕获网络异常
□ 在请求失败时自动重试一次
□ 打印清晰的错误信息，包括页码和错误类型
第三优先级：数据存储格式扩展
□ 支持保存为CSV文件（你已实现）
□ 同时支持保存为JSON文件（新增功能）
□ 在文件顶部自动添加表头（CSV）或格式（JSON）
第四优先级：运行信息与调试
□ 打印当前正在爬取的页码
□ 打印本页解析到的书籍数量
□ 打印累计总条数
□ 保存完成后打印“保存成功”信息
第五优先级（可选）
□ 添加进度条（tqdm 库）
□ 支持 --output 参数自定义文件名
□ 支持 --delay 参数自定义请求间隔
￼
你现在要做的事
1. 先打开你现有的 book_spider.py，确认它当前已经实现了哪些功能。
2. 对照上面的清单，从第一优先级的任务开始逐项实现。
3. 每完成一项，运行一次代码确认功能正常。
4. 全部完成后，把代码发给我检查。
你不需要一次性完成所有功能，先完成“自动翻页与参数化”部分，也就是接收起始页和结束页参数并循环请求。完成后告诉我结果，我们再继续下一项。
"""

import sys
import csv
import json
import requests
from bs4 import BeautifulSoup
import time
class Html(object):
    def __init__(self,start_page,end_page):
        self.start_page = start_page
        self.end_page = end_page
        self.url = f"https://books.toscrape.com/catalogue/page-{{}}.html"
        self.headers = {
    "User‑Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept‑Language": "zh‑CN,zh;q=0.9",
    "Accept‑Encoding": "gzip, deflate, br",
    "Referer": "https://www.baidu.com",
    "Connection": "keep‑alive",
    "Upgrade‑Insecure‑Requests": "1",
    "Cache‑Control": "max‑age=0",
    "sec‑ch‑ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
    "sec‑ch‑ua‑platform": "\"Windows\""
}
        self.data = []
    def fetch(self,DangQian_page):
        url=self.url.format(DangQian_page)
        try:
            response = requests.get(url,self.headers)
            response.encoding = "utf-8"
            response.raise_for_status()
            print("请求成功，状态码：", response.status_code)
            return BeautifulSoup(response.text,"html.parser")
        except requests.exceptions.HTTPError as err:
            print(f"第{DangQian_page}页HTTP请求错误: {err}")
        except Exception as e:
            print(f"第{DangQian_page}页网络异常: {e}")
    def parse(self,soup):
        itmes = soup.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3")
        for index,itme in enumerate(itmes,start=1):
            mingzi=itme.h3.a["title"]
            jiege = itme.select_one(".price_color").get_text(strip=True)
            xianhuo =itme.select_one('p.instock.availability').get_text(strip=True)
            self.data.append([index,mingzi,jiege,xianhuo])
    def csv(self):
        with open("book.csv","w+",encoding="utf-8",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["序号", "书名", "价格", "库存"])
            for item in self.data:
                writer.writerow(item)
    def json(self):
        data_list = []
        for item in self.data:
            data_dict={"序号": item[0],"书名": item[1],"价格": item[2],"库存": item[3]}
            data_list.append(data_dict)
        with open("book.json","w",encoding="utf-8",newline="") as f:
            json.dump(data_list,f,ensure_ascii=False,indent=4)
    def run(self):
        for page in range(self.start_page,self.end_page+1):
            soup = self.fetch(page)
            print(f"正在处理第{page}页")
            if soup:
                self.parse(soup)
                time.sleep(0.5)
        self.csv()
        self.json()
if __name__ == "__main__":
    start = 1
    end = 2
    if len(sys.argv) ==3:
        start_page = int(sys.argv[1])
        end_page = int(sys.argv[2])
    else:
        start_page=start
        end_page=end

    html = Html(start_page=start_page, end_page=end_page)
    html.run()