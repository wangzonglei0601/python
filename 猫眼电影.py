import requests
from bs4 import BeautifulSoup
import csv
import time

class MaoyanScraper:
    def __init__(self, start_page=1, max_pages=2):
        self.start_page = start_page
        self.max_pages = max_pages
        self.current_page = start_page
        self.data = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Cookie": "你的Cookie",  # 如果运行时被拦截，再替换成真实Cookie
            "Referer": "https://www.maoyan.com/board/4",
        }

    def get_url(self):
        offset = (self.current_page - 1) * 10
        return f"https://www.maoyan.com/board/4?offset={offset}"

    def fetch(self):
        try:
            time.sleep(2)
            response = requests.get(self.get_url(), headers=self.headers, timeout=10)
            response.encoding = "utf-8"
            if "猫眼验证中心" in response.text:
                print("⚠️ 被反爬拦截，需要更新Cookie")
                return None
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def parse(self, soup):
        if soup is None:
            return
        items = soup.find_all("dd")
        print(f"第{self.current_page}页，找到{len(items)}部电影")
        for idx, item in enumerate(items, start=1):
            name = item.find("p", class_="name").find("a")["title"]
            score_integer = item.find("p", class_="score").find("i", class_="integer").text
            score_fraction = item.find("p", class_="score").find("i", class_="fraction").text
            score = score_integer + score_fraction
            star = item.find("p", class_="star").text.strip().replace("主演：", "")
            release = item.find("p", class_="releasetime").text.strip().replace("上映时间：", "")
            global_index = (self.current_page - 1) * 10 + idx
            self.data.append([global_index, name, score, star, release])

    def save(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["序号", "电影名", "评分", "主演", "上映时间"])
            writer.writerows(self.data)
        print(f"已保存{len(self.data)}条数据到{filename}")

    def run(self):
        while self.current_page <= self.start_page + self.max_pages - 1:
            print(f"正在爬取第{self.current_page}页...")
            soup = self.fetch()
            if soup:
                self.parse(soup)
                self.current_page += 1
            else:
                print("等待5秒后重试...")
                time.sleep(5)
        self.save(f"maoyan_{self.start_page}_{self.start_page+self.max_pages-1}.csv")

if __name__ == "__main__":
    scraper = MaoyanScraper(start_page=1, max_pages=2)
    scraper.run()