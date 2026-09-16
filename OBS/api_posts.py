import json
import requests
import time
import sys


class PostSpider(object):
    def __init__(self, start_page, max_page):
        self.start_page = start_page
        self.max_page = max_page
        self.current_page = start_page
        self.url = "https://jsonplaceholder.typicode.com/posts"
        self.headers = {
            "authority": "jsonplaceholder.typicode.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
        }
        self.result_data = {}

    # 请求数据
    def fetch_data(self, page):
        max_retry = 3
        for retry_count in range(1, max_retry + 1):
            try:
                print(f"开始请求第{page}页")
                response = requests.get(self.url, headers=self.headers, params={"_page": page}, timeout=5)
                response.encoding = "utf-8"
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"第{page}页请求错误，已重试{retry_count}次，错误信息：{e}")
                if retry_count < max_retry:
                    wait_time = retry_count * 2
                    print(f"{wait_time}秒后重试，请等待...")
                    time.sleep(wait_time)
        print(f"第{page}页重试{max_retry}次全部失败，跳过该页")
        return None

    # 解析数据
    def parse_data(self, page_data):
        if not page_data:
            return None
        for item in page_data:
            post_id = item.get("id")
            if not post_id is None:
                self.result_data[post_id] = {
                    "title": item.get("title"),
                    "body": item.get("body")
                }

        return None

    # 保存为JSON文件
    def save_to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.result_data, f, ensure_ascii=False, indent=4)

    # 主执行方法
    def run(self):
        for page in range(self.start_page, self.max_page + 1):
            page_response = self.fetch_data(page)
            if page_response:
                self.parse_data(page_response)
        time.sleep(1)
        self.save_to_json(f"数据_{self.start_page}_{self.max_page}.json")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        start = 1
        end = 2

    spider = PostSpider(start_page=start, max_page=end)
    spider.run()
