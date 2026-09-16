import csv
import requests
from bs4 import BeautifulSoup
import sys
import time
class Book(object):
    def __init__(self,start_page,max_page):
        self.start_page = start_page
        self.max_page = max_page
        self.current_page = start_page
        self.result_data = []
        # self.url = "https://www.maoyan.com/board/4?offset=0"
        self.headers = {
            "Cookie":"__mta=45530907.1780514883894.1781037960284.1781038240918.20; uuid_n_v=v1; "
                     "uuid=55DF70D05F8211F1BFAEAD289BCE1CE2CE3523EF787A4EACAE964E51229B681A; _lx_"
                     "utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_cuid=19e8ef508b1c8-0e"
                     "8970383077b58-4c657b58-168000-19e8ef508b1c8; _lxsdk=55DF70D05F8211F1BFAEAD2"
                     "89BCE1CE2CE3523EF787A4EACAE964E51229B681A; _ga=GA1.1.225729017.1780514884;"
                     " global-guide-isclose=true; __mta=45530907.1780514883894.1781018468393.178"
                     "1018473940.7; _csrf=d6378c74ca7664e6d05c39354d9d69b5de5452b5dba533abde183f1"
                     "fa58ef169; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1781018188,1781018542,17"
                     "81037822,1781038241; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1781038241; H"
                     "MACCOUNT=582A1114C861AF28; _ga_WN80P4PSY7=GS2.1.s1781037162$o4$g1$t17810382"
                     "40$j33$l0$h0; _lxsdk_s=19eae165e3e-e40-cbb-f81%7C%7C15",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, lik"
                         "e Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
        }
    # 构造网页
    def get_url(self):
        offset = (self.current_page - 1) * 10
        return f"https://www.maoyan.com/board/4?offset={offset}"
    #请求网页
    def fetch(self):
        try:
            response = requests.get(self.get_url(),headers=self.headers,timeout=5)
            response.encoding = "utf-8"
            if"猫眼验证中心" in response.text:
                print("被反扒，请更新【Cookie】")
                return None
            soup = BeautifulSoup(response.text,"html.parser")
            return soup
        except Exception as e:
            print(f"请求失败{e}")
            return None
    # 解析网页
    def parse(self,soup):
        if soup is None:
            return None
        zong = soup.find_all("dd")
        print(f"第{self.current_page}页，找到{len(zong)}数据")
        for index,i in enumerate(zong,start=1):
            name = i.find("p",class_="name").find("a")["title"]
            ping =i.find("p",class_="score").find("i",class_="integer").text
            ping1 =i.find("p",class_="score").find("i",class_="fraction").text
            pingfen = ping + ping1
            zhuyan = i.find("p",class_="star").text.strip().replace("主演：","")
            shijian =i.find("p",class_="releasetime").text.strip().replace("上映时间：","")
            global_index = (self.current_page - 1) * 10 +index
            self.result_data.append([global_index,name,pingfen,zhuyan,shijian])
        return None
    # 保存csv
    def save_to_csv(self,filename):
        with open(filename,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["序号","电影","评分","主演","时间"])
            writer.writerows(self.result_data)
        print(f"已保存{filename}文件，{len(self.result_data)}条数据")
    # 主程序
    def run(self):
        while self.current_page <= self.start_page +self.max_page-1:
            print(f"正在获取第{self.current_page}页数据")
            soup = self.fetch()
            if soup:
                self.parse(soup)
                self.current_page += 1
            else:
                print("请求失败请等待5秒")
                time.sleep(5)
        self.save_to_csv(f"猫眼{self.start_page}_{self.max_page+self.start_page-1}.csv")
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        start_page = int(sys.argv[1])
        max_page = int(sys.argv[2])
    else:
        start_page = 1
        max_page = 2
    book = Book(start_page=start_page,max_page=max_page)
    book.run()
