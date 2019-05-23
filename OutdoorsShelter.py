import urllib
import http.client


conn = http.client.HTTPConnection("apis.data.go.kr")
conn.request("GET","/1741000/EarthquakeOutdoorsShelter/getEarthquakeOutdoorsShelterList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=10&flag=Y&type=xml")
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))

