from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

class ZLSpider:
    def __init__(self):
        self.data = []
        # 目标第一页url
        self.page_url = "https://sou.zhaopin.com/?jl=489&kw=python&p=1"

    def run(self):
        with sync_playwright() as p:
            # 启动浏览器，关闭无头可看界面调试 headless=False
            browser = p.chromium.launch(headless=True)
            # 新建页面，模拟真人设备
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
            )
            # 访问页面，自动等待页面加载完成
            page.goto(self.page_url, timeout=30000)
            # 等待岗位卡片渲染出来（关键：等待动态DOM加载）
            page.wait_for_selector("div.joblist-box__item", timeout=15000)
            # 获取浏览器渲染完成后的完整网页源码
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            self.parse(soup)
            browser.close()
        self.save_csv()

    def parse(self, soup):
        job_items = soup.find_all("div", class_="joblist-box__item")
        print(f"页面识别到 {len(job_items)} 条岗位")
        for item in job_items:
            # 职位名称
            title_tag = item.find("a", class_="jobinfo__name")
            job_title = title_tag.get_text(strip=True) if title_tag else "无"
            # 公司名称
            comp_tag = item.find("a", class_="companyinfo__name")
            company = comp_tag.get_text(strip=True) if comp_tag else "无"
            # 薪资
            salary_tag = item.find("p", class_="jobinfo__salary")
            salary = salary_tag.get_text(strip=True) if salary_tag else "面议"
            # 工作地点
            area_tag = item.find("span", class_="jobinfo__area")
            area = area_tag.get_text(strip=True) if area_tag else "无"
            # 学历要求
            edu_tag = item.find("span", class_="jobinfo__deg")
            edu = edu_tag.get_text(strip=True) if edu_tag else "不限"

            self.data.append({
                "职位名称": job_title,
                "公司名称": company,
                "薪资范围": salary,
                "工作地点": area,
                "学历要求": edu
            })

    def save_csv(self):
        headers = ["职位名称", "公司名称", "薪资范围", "工作地点", "学历要求"]
        with open("智联一页Python岗位.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.data)
        print(f"抓取完成，共{len(self.data)}条数据，已保存CSV")

if __name__ == '__main__':
    spider = ZLSpider()
    spider.run()