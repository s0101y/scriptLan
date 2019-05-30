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

MAP = []
Mname = []
tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")    # item 엘리먼트 리스트 추출

for item in itemElements:
    name = item.find("clnsShuntFcltyNm")  # clnsShuntFcltyNm 검색
    longitude = item.find("latitude")  # latitude 검색
    latitude = item.find("hardness")  # hardness 검색

    if len(name.text) > 0:  # 검색된 결과가 있다면
        Mname.append([name.text])  # 하나의 구호소 이름

    if len(latitude.text) > 0:  # 검색된 결과가 있다면
        MAP.append([longitude.text, latitude.text])  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 TEXT에 append

for a in range(len(MAP)):
    MAP[a] = [float(x) for x in MAP[a]]

Mname = sum(Mname, [])

print(MAP)

import folium
# 위도 경도 지정
map_osm = folium.Map (location=MAP[0], zoom_start=13)
# 마커 지정
for a in range(len(MAP)):
    folium.Marker(MAP[a], popup=Mname[a]).add_to(map_osm)
# html 파일로 저장
map_osm.save('osm.html')