import requests
import csv

def get_maotai_rest(page):
    url = f"https://www.dianping.com/zunyi{page}"  # 这里替换成你的真实目标url
    # 全部手敲，使用标准英文减号 -，杜绝特殊字符报错
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"第{page}页请求出错：{e}")
        return None


def save_csv(data_list):
    with open("book_data.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["书名", "价格"])
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == "__main__":
    all_data = []
    max_page = 3
    for p in range(1, max_page + 1):
        print(f"正在抓取第{p}页")
        data = get_maotai_rest(page=p)
        if not data:
            continue

        # =========这里根据网站返回json，修改解析逻辑=========
        # for item in data["list"]:
        #     book = {
        #         "书名": item["title"],
        #         "价格": item["price"]
        #     }
        #     all_data.append(book)

    save_csv(all_data)
    print("抓取完成，已保存 book_data.csv")
