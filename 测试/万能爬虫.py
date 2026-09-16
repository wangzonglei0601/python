"""
通用静态网页爬虫模板
适用：无JS渲染的静态HTML页面
功能：分页爬取、自定义CSS选择器提取字段、utf-8-sig编码CSV导出
依赖：requests, beautifulsoup4
安装依赖：pip install requests beautifulsoup4
"""
import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urlparse, urljoin



class paconglei(object):
    def __init__(self,起始网址,每条选择器,字段列表,分页选择器=None):
        self.起始网址 = 起始网址
        self.每条选择器 = 每条选择器
        self.字段列表 = 字段列表
        self.分页选择器 = 分页选择器
        self.数据列表=[]
        self.请求头 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    def 获取网页(self,网址):
        try:
            响应=requests.get(网址,headers=self.请求头,timeout=5)
            响应.encoding="utf-8"
            响应.raise_for_status()
            响应对象 =BeautifulSoup(响应.text,"html.parser")

            return 响应对象
        except Exception as e:
            print(f"请求失败！网址：{网址}，错误：{e}")
            # 请求失败，返回空值
            return None
    def 解析网页当前页码(self,解析对象):
        所有数据块=解析对象.select(self.每条选择器)
        if not 所有数据块:
            print(f"警告：选择器 {self.每条选择器} 没有匹配到内容！")
        for 数据块 in 所有数据块:
            一条数据 = {}
            for 字段配置 in self.字段列表:
                字段选择器=字段配置["名字选择器"]
                类型=字段配置.get("内容类型","文本")
                标签=数据块.select_one(字段选择器)
                if 标签:
                    if 类型 =="文本":
                        取出字= 标签.get_text(strip=True)
                    else:
                        取出字=标签.get(类型,"")

                else:
                    取出字=""
                一条数据[字段配置["字段名称"]]=取出字
            self.数据列表.append(一条数据)
        print(f"本页解析{len(所有数据块)}条，累计共{len(self.数据列表)}")
    def 获取下一页网址(self,解析对象):
        if self.分页选择器 is None:
            return None
        下一页标签 =解析对象.select_one(self.分页选择器)
        if 下一页标签 and 下一页标签.get("href"):
            完整网页 = urljoin(self.起始网址,下一页标签["href"])
            return  完整网页
        return None
    def 保存(self,文件名称="结果数据.csv"):
        if not self.数据列表:
            print("没有爬取到数据，不保存文件")
            return None
        表头列表=[配置["字段名称"] for 配置 in self.字段列表]
        with open(文件名称,"w",newline="",encoding="utf-8-sig") as f:
            写入对象 = csv.DictWriter(f,fieldnames=表头列表)
            写入对象.writeheader()
            写入对象.writerows(self.数据列表)
            print(f"保存完成！共 {len(self.数据列表)} 条数据，文件：{文件名称}")
    def 运行程序(self,最大页数=None):
        当前网址= self.起始网址
        当前页数=1
        while 当前网址:
            print(f"\n===== 正在爬取第 {当前页数} 页：{当前网址} =====")
            页面解析对象 = self.获取网页(当前网址)
            if not 页面解析对象:
                break
            self.解析网页当前页码(页面解析对象)
            当前网址 =self.获取下一页网址(页面解析对象)
            当前页数 += 1
            time.sleep(1)
            if 最大页数 is not None and 当前页数>最大页数:
                print(f"已到达最大页数 {最大页数}，爬虫停止")
                break
        self.保存()
# 程序入口：直接运行这个文件时，下面代码才会执行
if __name__ == "__main__":
    # 1. 创建爬虫对象，传入所有配置参数
    ceShiPaChong = paconglei(
        起始网址="https://books.toscrape.com/catalogue/page-1.html",
        每条选择器=".product_pod",
        # 定义要提取的字段规则
        字段列表=[
            {
                "字段名称": "图书名称",
                "名字选择器": "h3 a",
                "内容类型": "title"
            },
            {
                "字段名称": "图书价格",
                "名字选择器": ".price_color",
                "内容类型": "文本"
            }
        ],
        分页选择器=".next a"
    )

    # 2. 启动爬虫，限制最多爬3页
    ceShiPaChong.运行程序(最大页数=3)