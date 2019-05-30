import urllib
import http.client


conn = http.client.HTTPConnection("apis.data.go.kr")
conn.request("GET","/B552016/PublicFacilSafetyMngService/getPublicFacilSafetyMngList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=1&pageNo=1&type=xml&facilNo=AR1974-0000015&facilNm=1-002%20%EC%84%9C%EC%9A%B8%EC%97%AD&facilAddr=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C")
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))


#http://apis.data.go.kr/B552016/PublicFacilSafetyMngService/getPublicFacilSafetyMngList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=1&pageNo=1&type=json&facilNo=AR1974-0000015&facilNm=1-002%20%EC%84%9C%EC%9A%B8%EC%97%AD&facilAddr=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C

#http://apis.data.go.kr/1741000/DisasterMsg2/getDisasterMsgList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=10&type=xml&flag=Y
