from urllib.request import urlopen
url = "http://www.baidu.com"
resp = urlopen(url)
# print(resp)
with open("baidu12.html","w",encoding="utf-8") as f:
    content = resp.read().decode('utf-8')
    f.write(content)
    print(content)