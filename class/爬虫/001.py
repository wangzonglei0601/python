from pydoc import text

import requests
url ="https://pss.bdstatic.com/static/superman/img/topnav/newfanyi-da0cea8f7e.png"
response = requests.get(url)
response.encoding = 'utf-8'
response.raise_for_status()
if response.status_code == 200:

    errr=response.content
    with open('baidu.jpg', 'wb') as f:
        f.write(errr)