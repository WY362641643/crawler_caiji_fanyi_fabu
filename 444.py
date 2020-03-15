import requests

res = requests.get('http://www.baidu.com/link?url=ZHqOqrsVPRpYMVUg8vuaO_1bJMO3-dhqvSMatHJf54Cs2UfVxephF79rZIkmqYjjyGfdKQ2E31Hz6SFp60sRzzeBXDldbjs14J4Foa5sR7y')
if res.status_code == 200:
    r = res.url
    print(res.text)