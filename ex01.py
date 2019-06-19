import http.client
import urllib
import webbrowser
import folium
from xml.etree import ElementTree
import matplotlib.pyplot as plt

server = "apis.data.go.kr"
conn = http.client.HTTPConnection(server)
hangul_utf8 = urllib.parse.quote("서울특별시 송파구")
conn.request("GET", "/B552016/OldFacilService/getFacil30YearsOldList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=20&pageNo=1&type=xml&facilAddr="+hangul_utf8)
#http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
req = conn.getresponse()
print(req.status)
if int(req.status) == 200:
    strXml = req.read()
else:
    print("failed!")
MAP = []
MAP1 = []
Grade = []
Mname = []
tree = ElementTree.fromstring(strXml)
itemElements = tree.getiterator("item")    # item 엘리먼트 리스트 추출

for item in itemElements:
    name = item.find("facilNm")  # clnsShuntFcltyNm 검색
    grade = item.find("sfGrade")
    latitude = item.find("gisX")
    longitude = item.find("gisY")


    if len(name.text) > 0:      # 검색된 결과가 있다면
        Mname.append(name.text)  # 하나의 구호소 이름
        Grade.append(grade.text)  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 TEXT에 append
        MAP.append(longitude.text)
        MAP1.append(latitude.text)

gCount = [0,0,0,0]
z=[]
z1=[]
for e in MAP:
    if e is not None and len(e) > 0:
        z.append(e)
MAP = z
for e in MAP1:
    if e is not None and len(e) > 0:
        z1.append(e)
MAP1 = z1

print(MAP)
print(MAP1)

for a in range(len(MAP)):
        MAP = [float(x) for x in MAP]
        MAP1 = [float(x) for x in MAP1]

fin = []

for a in range(len(MAP)):
    fin.append([MAP[a], MAP1[a]])

print(Mname)
print(Grade)
print(MAP)
print(MAP1)
print(fin)
#Dmap.save('dangerMap.html')  # html 파일로 저장
#webbrowser.open('dangerMap.html')

for a in range(len(Grade)):
    if Grade[a] == 'A등급':
        gCount[0] += 1
for a in range(len(Grade)):
    if Grade[a] == 'B등급':
        gCount[1] += 1
for a in range(len(Grade)):
    if Grade[a] == 'C등급':
        gCount[2] += 1
for a in range(len(Grade)):
    if Grade[a] == 'D등급':
        gCount[3] += 1

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

GradeN = ['A등급', 'B등급', 'C등급', 'D등급']

xs = [i for i, _ in enumerate(GradeN)]
plt.bar(xs, gCount)
plt.ylabel("건물 개수")
plt.title("노후건물 안전등급 현황")

plt.xticks([i for i, _ in enumerate(GradeN)], GradeN)
plt.show()


