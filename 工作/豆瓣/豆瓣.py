# https://movie.douban.com/top250
import sys
import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm
class Item(object):
    def __init__(self,strat_page,max_page,url_page=None):
        self.strat_page=strat_page
        self.base_url = url_page
        self.max_page=max_page
        self.url=url_page
        self.data=[]
        self.headers_page ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
            "Cookie":"bid=_G5dyP0z_fQ; _pk_id.100001.4cf6=d0c5437a1205fc47.1782075413.; __utm"
                     "c=30149280; __utmz=30149280.1782075413.1.1.utmcsr=(direct)|utmccn=(direc"
                     "t)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1782075413.1.1.utmc"
                     "sr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=orrTTEWRUzbTF4K8D6"
                     "ZhoGsGwlYCunFo; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.568553"
                     "13.1782075413.1782075413.1782119504.2; __utmb=30149280.0.10.1782119504; "
                     "__utma=223695111.385826990.1782075413.1782075413.1782119504.2; __utmb=22"
                     "3695111.0.10.1782119504"
        }
    def run(self):
        page_range = range(self.strat_page, self.max_page + 1)
        # desc：进度条文字；unit：单位；ncols：进度条宽度
        pbar = tqdm(page_range, desc="正在爬取电影页面", unit="页",ncols=100)
        # page_num =range(self.strat_page, self.max_page + 1)
        # pages=tqdm(page_num,desc="正在爬取网页",unit="页",ncols=90)
        for page_num in pbar:
            if page_num ==1:
                self.url=self.base_url
            # start = (page_num - 1) * 25
            # self.url = f"{self.base_url}?start={start}"
            else:
                start = page_num - 1
                self.url = f"https://www.dygod.net/html/gndy/dyzz/index_{start}.html"
            try:
                response=requests.get(self.url,headers=self.headers_page,timeout=5)
                response.encoding="gbk"
                response.raise_for_status()
                print("网页正常200",self.url)
                soup=BeautifulSoup(response.text,"html.parser")
            except Exception as e:
                print(e)
                continue
            itmes = soup.select(".tbspan")
            try:
                for itme in itmes:
                    itmes = itme.select_one(".ulink")
                    if itmes:
                        name = itmes.text.strip().replace("\xa0","")
                        lind = "https://www.dygod.net"+itmes["href"]
                        # print(lind)******************
                        self.data.append([name,lind])
                    # mingzi=itme.select(".title")
                    # zhongwen=mingzi[0].text.strip().replace("\xa0","")
                    # if len(mingzi)>1:
                    #     yingwen=mingzi[1].text.strip().replace("/","").replace("\xa0","") #if len(mingzi)>1 else ""
                    # else:
                    #     yingwen =""
                    # print(zhongwen,yingwen)
                    # self.data.append([zhongwen,yingwen])
            except Exception as e:
                print(e)
            next_link = soup.select_one(".next a")
            if next_link:
                xiayiye = next_link.get("href")
                zongye = self.base_url + xiayiye
                print(zongye)
            else:
                print(f"爬取完成，当前第{page_num}页")
            time.sleep(1)
        # file_name = f"{self.strat_page}-{self.max_page}.csv"
        save_path = r"C:\Users\14478\Desktop\豆瓣爬取结果.csv"
        with open(save_path,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["中文名", "详情页链接"])
            writer.writerows(self.data)
if __name__ == "__main__":
    if len(sys.argv)>2:
        strat_page = int(sys.argv[1])
        max_page = int(sys.argv[2])

    else:
        strat_page = 1
        max_page = 10
    item=Item(strat_page=strat_page,
              max_page=max_page,
              url_page="https://www.dygod.net/html/gndy/dyzz/index.html"
              )
    item.run()

