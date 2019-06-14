import http.client
import urllib
import webbrowser
import folium
from xml.etree import ElementTree

server = "apis.data.go.kr"
conn = http.client.HTTPConnection(server)
hangul_utf8 = urllib.parse.quote("서울특별시 강동구")
conn.request("GET", "/B552016/OldFacilService/getFacil30YearsOldList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=20&pageNo=1&type=xml&facilAddr="+hangul_utf8)
#http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
req = conn.getresponse()
print(req.status)
if int(req.status) == 200:
    strXml = req.read()
else:
    print("failed!")

Grade = []
Mname = []
MAP = []
tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")    # item 엘리먼트 리스트 추출

for item in itemElements:
    name = item.find("facilNm")  # clnsShuntFcltyNm 검색
    grade = item.find("sfGrade")
    latitude = item.find("gisX")  # hardness 검색
    longitude = item.find("gisY")  # latitude 검색

    if len(name.text) > 0:      # 검색된 결과가 있다면
        Mname.append(name.text)  # 하나의 구호소 이름
        MAP.append([longitude.text, latitude.text])  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 MAP에 append

    for a in range(len(MAP)):
        MAP[a] = [float(x) for x in MAP[a]]

    if len(grade.text) > 0:     # 검색된 결과가 있다면
        Grade.append(grade.text)  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 TEXT에 append


Dmap = folium.Map(location=MAP[0], zoom_start=15)  # 위도 경도 지정

for a in range(len(MAP)):
        folium.CircleMarker(MAP[a], radius=100, color='#ff2121', fill_color='#ff2121').add_to(Dmap)  # 마커 지정



print(Mname)
print(Grade)
Dmap.save('dangerMap.html')  # html 파일로 저장
webbrowser.open('dangerMap.html')