import http.client
import urllib
from xml.etree import ElementTree

server = "api.data.go.kr"
conn = http.client.HTTPConnection(server)
hangul_utf8 = urllib.parse.quote("서울특별시 강동구")
conn.request("GET", "/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm="+hangul_utf8)
#http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
req = conn.getresponse()
print(req.status)
if int(req.status) == 200:
    strXml = req.read()
else:
    print("failed!")

howmany = []
tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")    # item 엘리먼트 리스트 추출

for item in itemElements:
    acceptNum = item.find("aceptncPosblCo")  # aceptncPosblCo 검색
    if len(acceptNum.text) > 0:  # 검색된 결과가 있다면
        howmany.append([acceptNum.text])  # 수용인원

for a in range(len(howmany)):
    howmany[a] = [int(x) for x in howmany[a]]

howmany = sum(howmany, [])

print(howmany)
Count = [0,0,0,0,0]

for a in range(len(howmany)):
    if howmany[a] <= 500:
        Count[0] += 1
for a in range(len(howmany)):
    if (howmany[a] <= 1000 and howmany[a] > 500):
        Count[1] += 1
for a in range(len(howmany)):
    if (howmany[a] <= 5000 and howmany[a] > 1000):
        Count[2] += 1
for a in range(len(howmany)):
    if (howmany[a] <= 10000 and howmany[a] > 5000):
        Count[3] += 1
for a in range(len(howmany)):
    if (howmany[a] <= 20000 and howmany[a] > 10000):
        Count[4] += 1

print(Count)

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

plt.suptitle('대피소 수용 인원', fontsize=16)
b = ["500명 이하", "1000명 이하", "5000명 이하","10000명 이상","20000명이상"]
plt.pie(Count, labels=b, shadow=True, autopct='%1.1f%%')
plt.show()