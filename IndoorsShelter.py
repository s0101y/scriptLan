import urllib
import http.client


conn = http.client.HTTPConnection("apis.data.go.kr")
hangul_utf8 = urllib.parse.quote("한국산업기술대학교")
conn.request("GET","/1741000/EarthquakeIndoors/getEarthquakeIndoorsList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=10&type=xml&flag=Y")
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))
