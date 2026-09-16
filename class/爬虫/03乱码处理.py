import requests
URL = 'http://www.baidu.com'
response = requests.get(URL)
if response.status_code == 200:
    # response.encoding = 'utf-8'
    res = response.content
    # response.encoding = 'utf-8'
    text = res.decode('utf-8')
    with open('baidu12.html', 'w',encoding='utf-8') as f:
        f.write(text)