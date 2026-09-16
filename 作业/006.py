import csv

leibiao = [
    {"title": "文章1", "author": "张三"},
    {"title": "文章2", "author": "李四"},
    {"title": "文章3", "author": "王五"}
]
with open("data.csv", 'w', encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, ("title", "author"))
    writer.writeheader()
    writer.writerows(leibiao)
import csv

leibiao = [
    {"目录": "文章1", "作者": "张三"},
    {"title": "文章2", "author": "李四"},
    {"title": "文章3", "author": "王五"},
]

new_data = []
for item in leibiao:
    title_val = item.get("目录", item.get("title"))
    author_val = item.get("作者", item.get("author"))
    # 拼接成字符串，只一个key
    new_data.append({"内容": f"{title_val}|{author_val}"})

with open("data.csv", 'w', encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, ["内容"])
    writer.writeheader()
    writer.writerows(new_data)