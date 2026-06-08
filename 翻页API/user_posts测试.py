# 导入网络请求库
import requests
# 导入json处理库，用于保存数据
import json
# 导入时间库，用于延时和重试
import time
# 导入系统库，用于接收命令行参数
import sys

# 定义爬虫类，用于爬取文章数据
class Book(object):
    # 初始化方法，设置起始页、结束页、请求头、URL、存储数据的字典
    def __init__(self, start_page, end_page):
        self.start_page = start_page  # 起始页码
        self.end_page = end_page      # 结束页码
        self.headers = {              # 请求头，模拟浏览器访问
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                          " like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
            "authority": "jsonplaceholder.typicode.com"
        }
        self.url = "https://jsonplaceholder.typicode.com/posts"  # 目标接口地址
        self.result_data = {}  # 用于存储最终解析好的数据

    # 爬取单页数据，带重试机制
    def fetch_page(self, page):
        max_retry = 3  # 最大重试次数
        # 循环重试
        for i in range(1, max_retry + 1):
            try:
                # 发送GET请求，携带页码参数
                response = requests.get(self.url, headers=self.headers, params={"_page": page}, timeout=5)
                response.encoding = "utf-8"  # 设置编码
                response.raise_for_status()  # 如果请求失败，直接抛出异常
                return response.json()  # 返回json格式数据
            # 捕获所有异常
            except Exception as e:
                print(f"第{page}页请求失败，已重试{i}次，错误{e}")
                # 如果没达到最大重试次数，等待后再次请求
                if i < max_retry:
                    wait_time = i * 2
                    print(wait_time, "秒后重试...请等待")
                    time.sleep(wait_time)
        # 重试3次都失败，返回None
        return None

    # 解析一页的数据，提取id、标题、内容
    def parse_data(self, page_data):
        # 遍历当前页的每一条数据
        for item in page_data:
            data_id = item.get("id")  # 获取文章id
            # 以id为key，保存标题和内容
            self.result_data[data_id] = {
                "title": item.get("title"),
                "body": item.get("body")
            }

    # 将数据保存为json文件
    def save_to_json(self, filename):
        # 打开文件，写入数据
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.result_data, f, ensure_ascii=False, indent=2)
        # 打印保存成功提示
        print(f"\n✅ 保存完成：共 {len(self.result_data)} 条数据 -> {filename}")

    # 主运行方法：循环爬取多页 → 解析 → 保存
    def run(self):
        # 从起始页到结束页依次爬取
        for page in range(self.start_page, self.end_page + 1):
            page_data = self.fetch_page(page)  # 请求一页数据
            if page_data:  # 如果数据不为空
                self.parse_data(page_data)     # 解析数据
                print(f"✅ 第 {page} 页处理完成\n")
                time.sleep(1)  # 每页间隔1秒，友好爬取
        # 所有页面爬取完毕后保存文件
        self.save_to_json(f"{self.start_page}_{self.end_page}.json")

# 程序入口
if __name__ == "__main__":
    # 如果命令行传入了2个参数，就用传入的页码
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    # 否则默认爬取 1-2 页
    else:
        start = 1
        end = 2

    # 创建爬虫对象并开始运行
    spider = Book(start_page=start, end_page=end)
    spider.run()