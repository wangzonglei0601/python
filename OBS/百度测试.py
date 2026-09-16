'''
爬取百度实时热搜榜单
目标网址：https://top.baidu.com/board?tab=realtime
功能：自定义起始下标与抓取条数，提取热搜序号、标题、热度、链接，保存为json并控制台打印
'''
import csv
import json
import sys
import requests
from bs4 import BeautifulSoup


class BaiduHotSpider:
    """百度热搜爬虫类"""
    def __init__(self, start_index, fetch_count):
        """
        初始化爬虫
        :param start_index: 热搜起始下标（html元素下标从0开始）
        :param fetch_count: 需要抓取的热搜条数
        """
        # 起始截取下标
        self.start_index = start_index
        # 抓取条目总数
        self.fetch_count = fetch_count
        # 存储解析完成的热搜数据
        self.data_list = []
        # 目标百度热搜地址
        self.url = "https://top.baidu.com/board?tab=realtime"
        # 请求头，模拟浏览器访问，携带UA和Cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                          " like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
            "Cookie": "BAIDUID=77C2E17DDDE2848E5A3F9DB8B14D67C4:FG=1; BAIDUID_BFESS=77C2E17DD"
                      "DE2848E5A3F9DB8B14D67C4:FG=1; BIDUPSID=77C2E17DDDE2848E5A3F9DB8B14D67"
                      "C4; PSTM=1781045696; ZFY=fjJ6eyPabFYSmBx7mmQUYmeO7dl8zRoMaPxfFvd8:Bnw"
                      ":C; H_PS_PSSID=67862_68166_69000_69294_69593_69778_69921_69907_69961_7"
                      "0116_70156_70169_70408_70422_70478_70383_70611_70627_70793_70548_7054"
                      "6_70550_70494_70845_70907_70964_70969_70979_71029_71032_71050"
        }

    def fetch_html(self):
        """发送http请求，获取网页并生成BeautifulSoup解析对象"""
        try:
            # GET请求访问热搜页面，超时限制5秒
            response = requests.get(self.url, headers=self.headers, timeout=5)
            # 设置网页编码为utf-8，防止中文乱码
            response.encoding = "utf-8"
            # 状态码非200则抛出异常
            response.raise_for_status()
            print("网页正常200")
            # 用网页文本生成bs解析对象并返回
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        except Exception as e:
            # 请求异常打印错误信息
            print(f"网页错误{e}请求失败")

    def parse_html(self, soup_obj):
        """
        解析bs对象，提取热搜数据存入self.data_list
        :param soup_obj: fetch_html方法返回的BeautifulSoup对象
        """
        # 如果解析对象为空，直接退出解析
        if not soup_obj:
            return None
        # 匹配所有热搜条目容器
        all_hot_items = soup_obj.select(".category-wrap_iQLoo")
        # 根据起始下标和条数切片，截取需要的热搜
        target_items = all_hot_items[self.start_index: self.start_index + self.fetch_count]
        try:
            # 遍历截取的热搜，序号从1开始计数
            for display_id, item_tag in enumerate(target_items, start=1):
                # 提取标题并去除无用字符
                title = item_tag.select_one(".c-single-text-ellipsis").text.strip().replace(" div", "")
                # 提取热度数值
                hot_score = item_tag.select_one(".hot-index_1Bl1a").text.strip().replace(" div", "")
                # 提取热搜跳转链接
                link = item_tag.select_one("a")["href"]
                # 组装字典，添加到数据列表
                self.data_list.append({
                    "序号": display_id,
                    "标题": title,
                    "热度": hot_score,
                    "网址": link
                })
        except Exception as e:
            # 解析单条数据出错时打印提示
            print(f"解析网页{e}失败")

    def save_json(self, file_name):
        """
        将爬取的数据写入json文件
        :param file_name: 保存的文件名称
        """
        # 以写入模式打开文件，utf-8保证中文正常存储
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            # 序列化列表数据为json，不转义中文，缩进4格格式化输出
            json.dump(self.data_list, f, ensure_ascii=False, indent=4)

    def print_result(self):
        """控制台打印所有爬取到的热搜数据"""
        print("\n打印爬取结果")
        print("*" * 50)
        for item in self.data_list:
            print(item["序号"], item["标题"], item["热度"], item["网址"])

    def export_and_print(self):
        """统一执行保存文件 + 打印数据"""
        # 文件名格式：起始下标_抓取条数.json
        file_name = f"{self.start_index}_{self.fetch_count}.json"
        self.save_json(file_name)
        self.print_result()


if __name__ == "__main__":
    # 程序入口，命令行参数处理与爬虫执行
    # 判断命令行参数，如果参数>=3(脚本名+起始下标+抓取数量)，读取传入数值
    if len(sys.argv) >= 3:
        input_start = int(sys.argv[1])
        input_count = int(sys.argv[2])
    else:
        # 无足够参数，设置默认值
        input_start = 0
        input_count = 10

    # 实例化爬虫对象
    spider = BaiduHotSpider(start_index=input_start, fetch_count=input_count)
    # 请求网页获取bs对象
    soup_result = spider.fetch_html()
    # 请求成功才执行解析、保存、打印
    if soup_result:
        spider.parse_html(soup_result)
        spider.export_and_print()