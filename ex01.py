import http.client
import urllib
from xml.etree import ElementTree
server = "api.data.go.kr"
conn = http.client.HTTPConnection(server)
hangul_utf8 = urllib.parse.quote("부산광역시 북구")
conn.request("GET", "/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm="+hangul_utf8)
#http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
req = conn.getresponse()
print(req.status)
if int(req.status) == 200:
    strXml = req.read()
else:
    print("failed!")


tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")    # item 엘리먼트 리스트 추출
print(itemElements)

for item in itemElements:
    name = item.find("clnsShuntFcltyNm")          #clnsShuntFcltyNm 검색
    adr = item.find("rdnmadr")                      #rdnmadr 검색
    print(adr)
    if len(adr.text) > 0 :
        print({"name":name.text,"adr":adr.text})