'''
爬取百度实时热搜榜单
目标网址：https://top.baidu.com/board?tab=realtime
功能：获取前10条热搜的序号、标题、热度、链接，保存为CSV并控制台打印
'''
import csv
import sys
import requests
from bs4 import BeautifulSoup
import json


class BaiduHotSearch:
    """百度实时热搜爬虫类"""
    def __init__(self):
        # 目标请求地址
        self.url = "https://top.baidu.com/board?tab=realtime"
        # 请求头，模拟浏览器访问
        self.headers = {
            "Cookie": "BAIDUID=77C2E17DDDE2848E5A3F9DB8B14D67C4:FG=1; BAIDUID_BFESS=77C2E17DDDE"
                     "2848E5A3F9DB8B14D67C4:FG=1; BIDUPSID=77C2E17DDDE2848E5A3F9DB8B14D67C4; P"
                     "STM=1781045696; H_PS_PSSID=67862_68166_69000_69294_69593_69778_69921_6990"
                     "7_69961_69998_70013_70116_70156_70169_70408_70422_70478_70383_70446_7052"
                     "3_70611_70627_70793_70811_70548_70546_70550_70494_70845_70907_70964_70969"
                     "_70979_71029_71032; delPer=0; PSINO=6; BA_HECTOR=2l00ah2l812hal850g24802g"
                     "al8g201l2h6e128; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ZFY=fjJ6eyPabFYS"
                     "mBx7mmQUYmeO7dl8zRoMaPxfFvd8:Bnw:C",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
        }
        # 请求超时时间
        self.timeout = 10
        # 存储最终爬取的数据列表
        self.data_list = []

    def fetch_html(self):
        """发送网络请求，获取网页源码"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.encoding = "utf-8"  # 设置编码
            response.raise_for_status()  # 主动抛出请求异常
            print("请求成功，状态码：200")
            return response.text
        except Exception as e:
            print(f"网页请求失败：{e}")

    def parse_html(self, html):
        """解析网页源码，提取热搜数据"""
        # 无网页源码直接返回
        if not html:
            return
        # 初始化解析器
        soup = BeautifulSoup(html, "html.parser")
        # 选取前10条热搜条目
        hot_item_list = soup.select(".category-wrap_iQLoo")[:10]

        try:
            # 遍历每条热搜，索引从1开始计数
            for serial_num, item in enumerate(hot_item_list, start=1):
                # 提取标题、热度、跳转链接
                title = item.select_one(".c-single-text-ellipsis").text.strip()
                hot_value = item.select_one(".hot-index_1Bl1a").text.strip()
                link_url = item.select_one("a")["href"]

                # 组装字典存入数据列表
                self.data_list.append({
                    "序号": serial_num,
                    "标题": title,
                    "热度": hot_value,
                    "网址": link_url
                })
        except Exception as e:
            print(f"数据解析出错：{e}")

    def save_to_csv(self, file_name):
        """将数据保存为CSV文件"""
        # 打开文件，写入csv数据
        with open(file_name, "w", newline="", encoding="utf-8") as f:
        # json文件
            json.dump(self.data_list, f, ensure_ascii=False, indent=2)
        #     # 定义表头字段
        #     field_names = ["序号", "标题", "热度", "网址"]
        #     csv_writer = csv.DictWriter(f, fieldnames=field_names)
        #     # 写入表头
        #     csv_writer.writeheader()
        #     # 批量写入所有数据
        #     csv_writer.writerows(self.data_list)
        # # 保存完成后打印数据
        self.print_data()

    def print_data(self):
        """在控制台打印爬取到的所有数据"""
        print("\n开始打印爬取结果")
        print("*" * 50)
        for item in self.data_list:
            print(item["序号"], item["标题"], item["热度"], item["网址"])


if __name__ == "__main__":
    # 实例化爬虫对象
    spider = BaiduHotSearch()
    # 1. 获取网页源码
    html_content = spider.fetch_html()
    # 2. 解析、保存、打印数据
    if html_content:
        spider.parse_html(html_content)
        spider.save_to_csv("百度热点")