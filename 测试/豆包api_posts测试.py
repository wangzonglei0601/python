import sys
import json
import time
import requests

# 常量配置（统一管理，便于修改）
API_URL = "https://jsonplaceholder.typicode.com/posts"
REQUEST_TIMEOUT = 5
MAX_RETRY_TIMES = 3
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
    "authority": "jsonplaceholder.typicode.com"
}


class PostCrawler:
    """文章爬虫类：负责请求、解析、存储数据"""

    def __init__(self, start_page: int, end_page: int):
        self.start_page = start_page
        self.end_page = end_page
        self.collected_data = {}  # 存储最终数据

    def fetch_single_page(self, page: int) -> list | None:
        """请求单页数据，带重试机制"""
        for retry in range(1, MAX_RETRY_TIMES + 1):
            try:
                print(f"📄 第 {page} 页 - 第 {retry} 次请求")
                resp = requests.get(
                    url=API_URL,
                    headers=DEFAULT_HEADERS,
                    params={"_page": page},
                    timeout=REQUEST_TIMEOUT
                )
                resp.raise_for_status()  # 自动抛出 HTTP 错误
                return resp.json()

            except Exception as e:
                print(f"❌ 第 {page} 页 - 第 {retry} 次请求失败：{str(e)}")
                if retry < MAX_RETRY_TIMES:
                    wait_sec = retry * 2
                    print(f"⏳ {wait_sec} 秒后重试...")
                    time.sleep(wait_sec)

        print(f"🚫 第 {page} 页请求失败，已跳过")
        return None

    def parse_posts(self, post_list: list):
        """解析文章列表并保存到内存"""
        if not post_list:
            return

        for post in post_list:
            post_id = post.get("id")
            if not post_id:
                continue

            self.collected_data[post_id] = {
                "title": post.get("title", ""),
                "body": post.get("body", "")
            }

    def save_to_json(self, filename: str = "posts_result.json"):
        """将数据保存为 JSON 文件"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.collected_data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 保存完成：共 {len(self.collected_data)} 条数据 -> {filename}")

    def run(self):
        """启动爬虫主流程"""
        print(f"🚀 开始爬取：第 {self.start_page} 页 ~ 第 {self.end_page} 页\n")

        for page in range(self.start_page, self.end_page + 1):
            data = self.fetch_single_page(page)
            if data:
                self.parse_posts(data)

            print(f"✅ 第 {page} 页处理完成\n")
            time.sleep(1)

        self.save_to_json(  f"posts_{self.start_page}_{self.end_page}.json")


def main():
    """程序入口"""
    try:
        if len(sys.argv) >= 3:
            start = int(sys.argv[1])
            end = int(sys.argv[2])
        else:
            start, end = 1, 2

        crawler = PostCrawler(start_page=start, end_page=end)
        crawler.run()

    except ValueError:
        print("❌ 页码必须是数字！")
    except Exception as e:
        print(f"❌ 程序异常：{e}")


if __name__ == "__main__":
    main()