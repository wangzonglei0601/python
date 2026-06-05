# 去掉无用导入
import sys

import requests
import time
import csv
from bs4 import BeautifulSoup

class MaoYanMovie(object):
    def __init__(self, start_page, max_page):
        # 起始页码
        self.start_page = start_page
        # 要爬取的总页数
        self.max_page = max_page
        # 当前正在爬取的页码
        self.current_page = start_page
        # 存储所有爬取数据
        self.movie_data = []
        # 请求头：模拟浏览器访问，防止反爬
        # "你的Cookie",  # 如果运行时被拦截，再替换成真实Cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
            "cookie": "__mta=45530907.1780514883894.1780515730273.1780516201059.6; uuid_n_v=v1; uuid=55DF70D05F8211F1BFAEAD289BCE1CE2CE3523EF787A4EACAE964E51229B681A; _csrf=d01f24eb611248c9601b14a4b43093a1c3d20755caa4dd5a68dc1253af034ba3; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1780514884; HMACCOUNT=582A1114C861AF28; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_cuid=19e8ef508b1c8-0e8970383077b58-4c657b58-168000-19e8ef508b1c8; _lxsdk=55DF70D05F8211F1BFAEAD289BCE1CE2CE3523EF787A4EACAE964E51229B681A; _ga=GA1.1.225729017.1780514884; __mta=45530907.1780514883894.1780514883894.1780515208153.2; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1780516200; _ga_WN80P4PSY7=GS2.1.s1780514883$o1$g1$t1780516201$j59$l0$h0; _lxsdk_s=19e8ef508b1-154-c94-ea7%7C%7C12",
            "referer": "https://www.maoyan.com/board/4"
        }

    # 构造当前页的URL
    def get_url(self):
        return "https://www.maoyan.com/board/4?offset={}".format((self.current_page - 1) * 10)

    def fetch(self):
        url = self.get_url()
        max_retries =3
        for attempt  in range(1,max_retries+1):
            try:
                print(f"第{attempt}请求")
                response = requests.get(url, headers=self.headers,timeout=5)
                response.encoding="utf-8"
                if "猫眼验证中心" in response.text:
                    print("⚠️ 被反爬拦截，需要更新Cookie")
                    return None
                return BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                print(f"第{attempt}次请求失败{e}")
                if attempt < max_retries:
                    print(f"  等待 {attempt * 2} 秒后重试...")
                    time.sleep(attempt * 2)
        print(f"第 {self.current_page} 页请求失败，已重试 {max_retries} 次，跳过该页")
        return None
    # 请求网页并返回BeautifulSoup解析对象
    # def fetch(self):
    #     url = self.get_url()
    #     try:
    #         response = requests.get(url, headers=self.headers, timeout=5)
    #         response.encoding = "utf-8"
    #         # 判断是否触发猫眼验证
    #         if "猫眼验证中心" in response.text:
    #             print("⚠️ 被反爬拦截，需要更新Cookie")
    #             return None
    #         # 返回解析后的soup对象
    #         return BeautifulSoup(response.text, "html.parser")
    #     except:
    #         print("第{}页请求失败".format(self.current_page))
    #         return None

    # 解析网页数据
    def parse(self, soup):
        # 获取当前页所有电影条目
        movie_items = soup.find_all("dd")
        for index, item in enumerate(movie_items, start=1):
            # 电影名称
            movie_name = item.find("p", class_="name").find("a")["title"]
            # 电影评分（整数部分 + 小数部分）
            score_integer = item.find("p", class_="score").find("i", class_="integer").text
            score_fraction = item.find("p", class_="score").find("i", class_="fraction").text
            movie_score = score_integer + score_fraction
            # 主演信息
            movie_star = item.find("p", class_="star").text.strip().replace("主演：", "")
            # 上映时间
            release_time = item.find("p", class_="releasetime").text.strip().replace("上映时间：", "")
            # 全局排名（跨页连续序号）
            global_index = (self.current_page - 1) * 10 + index
            # 将一条数据存入列表
            self.movie_data.append([global_index, movie_name, movie_score, movie_star, release_time])

    # 保存数据到CSV文件
    def save_to_csv(self, file_name):
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(["序号", "电影名", "评分", "主演", "上映时间"])
            # 写入所有数据
            writer.writerows(self.movie_data)
        print(f"已保存{len(self.movie_data)}条数据到 {file_name}")

    # 爬虫主运行逻辑
    def run(self):
        end_page = self.start_page + self.max_page - 1
        while self.current_page <= end_page:
            print(f"正在爬取第{self.current_page}页...")
            # 获取页面解析对象
            soup = self.fetch()
            if soup:
                # 解析数据
                self.parse(soup)
                # 页码+1，爬取下一页
                self.current_page += 1
            else:
                # 请求失败，等待5秒重试
                print("等待5秒后重试...")
                time.sleep(5)
        # 爬取完成，保存文件
        self.save_to_csv(f"maoyan_{self.start_page}_{end_page}.csv")

if __name__ == "__main__":
    # 创建爬虫实例：从第1页开始，爬2页
    if len(sys.argv) >=3:
        start_page = int(sys.argv[1])
        max_page = int(sys.argv[2])
        scraper = MaoYanMovie(start_page=start_page, max_page=max_page)
    # 启动爬虫
        scraper.run()