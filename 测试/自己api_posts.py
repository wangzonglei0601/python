import sys
import requests
import time
import json


class Book(object):
    def __init__(self, start_page, max_page):
        self.start_page = start_page
        self.max_page = max_page
        self.current_page = start_page
        self.result_data = {}  # 原 data → 更明确
        self.api_url = "https://jsonplaceholder.typicode.com/posts"  # 原 url → 更明确
        self.request_headers = {  # 原 headers → 更明确
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                          " like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
            "authority": "jsonplaceholder.typicode.com"
        }

    # 请求网页
    def fetch_page(self, page_num):  # 原 page → page_num 更清晰
        url = self.api_url
        max_retries = 3
        for retry_count in range(1, max_retries + 1):  # 原 i → retry_count 重试次数
            try:
                print("第{}次请求".format(retry_count))
                response = requests.get(url, headers=self.request_headers, params={"_page": page_num}, timeout=5)
                response.encoding = "utf-8"
                return response.json()
            except Exception as e:
                print("第{}次请求失败{}".format(retry_count, e))
                if retry_count < max_retries:
                    print(f"  等待 {retry_count * 2} 秒后重试...")
                    time.sleep(retry_count * 2)
        print(f"第{page_num}页失败，第{max_retries}次重试，跳过该页")
        return None

    # 解析数据
    def parser(self, post_list):  # 原 soup → post_list 更准确（不是HTML，是文章列表）
        if not post_list:
            return None
        for post in post_list:  # 原 i → post 一篇文章
            title =  post["title"]
            body =  post["body"]
            self.result_data[post["id"]] = {"title": title, "body": body}
        return None

    # 保存到 JSON
    def save_to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.result_data, f, ensure_ascii=False, indent=2)
        print(f"已保存{len(self.result_data)}条数据到{filename}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        start = 1
        end = 2

    book = Book(start_page=start, max_page=end)
    for page in range(start, end + 1):  # 原 i → page 更清晰
        souo = book.fetch_page(page)  # 原 sou → page_data 更明确
        if souo:
            book.parser(souo)
        print(f"\n===== 第{page}页爬取完成 =====\n")
        time.sleep(1)
    book.save_to_json(f"posts_{start}_{end}.json")