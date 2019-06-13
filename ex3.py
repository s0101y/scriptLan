from tkinter import *
from tkinter import font
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
import http.client
import urllib
from xml.etree import ElementTree
import folium
import spam




global MAP, Mname
MAP = []
Mname = []
server = "apis.data.go.kr"
conn = http.client.HTTPConnection(server)
hangul_utf8 = urllib.parse.quote("부산광역시 북구")
conn.request("GET",
             "/B552016/PublicFacilSafetyMngService/getPublicFacilSafetyMngList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=100&pageNo=1&type=xml&facilAddr=" + hangul_utf8)
req = conn.getresponse()
if int(req.status) == 200:
    strXml = req.read()
else:
    print("failed!")

tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출

for item in itemElements:
    name = item.find("facilNm")  # facilNm 검색
    grade = item.find("sfGrade")  # sfGrade 검색
    longitude = item.find("gisY")  # gisX 검색
    latitude = item.find("gisX")  # gisY 검색
    if len(name.text) > 0:  # 검색된 결과가 있다면
        Mname.append([name.text])  # 하나의 구호소 이름 리스트 Mname에 append
        MAP.append([longitude.text, latitude.text])  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 MAP에 append

for a in range(len(MAP)):
    MAP[a] = [float(x) for x in MAP[a]]

Mname = sum(Mname, [])
map_osm = folium.Map(location=MAP[0], zoom_start=15)  # 위도 경도 지정

for a in range(len(MAP)):
    folium.Marker(MAP[a], popup=Mname[a]).add_to(map_osm)  # 마커 지정

map_osm.save('dangermap.html')  # html 파일로 저장

