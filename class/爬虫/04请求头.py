# import requests

# url = 'http://www.baidu.com'
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
#     # "cookie": "BAIDUID=77C2E17DDDE2848E5A3F9DB8B14D67C4:FG=1; BAIDUID_BFESS=77C2E17DDDE2848E5A3F9DB8B14D67C4:FG=1; BIDUPSID=77C2E17DDDE2848E5A3F9DB8B14D67C4; PSTM=1781045696; ZFY=fjJ6eyPabFYSmBx7mmQUYmeO7dl8zRoMaPxfFvd8:Bnw:C; BD_HOME=1; BD_UPN=12314753; BA_HECTOR=ala40ka0a12ka10425ag25802h2ha41l4o9c028; H_PS_PSSID=67862_68166_69294_70548_71093_71150_71139_71220_71277_71279_71274_71290_71303_71324_71342_71352_71364_71370_71233_71406_71393_71401_71431_71465_71476_71480_71452_71445_71437_71415_71243_71550_71539_71534_71532_71541_71543_71561_71564_71554_71556_71566_71615_71628_71642_71648_71653_71503_71685_71713_71794_71721_71754_71804_71834_71819",
#     "user-agent":"Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36"
# }
# response = requests.get(url, headers=headers)
# import random
#
# ua_list = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2277.98",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
# ]
#
# url= "http://www.baidu.com"
# random_ua = random.choice(ua_list)
# headers = {
#     "User-Agent": random_ua
# }
# response =requests.get(url, headers=headers,timeout=10)
# if response.status_code==200:
#     res = response.content
#     text = res.decode('utf-8')
#     with open('baidu12.html','w',encoding="utf-8") as f:
#         f.write(text)
#         print(headers)
import requests
import fake_useragent
ur = fake_useragent.UserAgent()
uat = ur.random
url= "http://www.baidu.com"
headers = {
    "User-Agent": uat,
}
response =requests.get(url, headers=headers,timeout=10)
if response.status_code==200:
    res = response.content
    text = res.decode('utf-8')
    with open('baidu4.html','w',encoding="utf-8") as f:
        f.write(text)
        print(headers)