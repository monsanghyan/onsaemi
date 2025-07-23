from fastapi import FastAPI
import redis
import uvicorn
import requests
import json

def current_location():
   here_req = requests.get("http://www.geoplugin.net/json.gp")
   crd = {}


   if (here_req.status_code != 200):
       print("현재좌표를 불러올 수 없음")
   else:
       location = json.loads(here_req.text)
       crd = {"lat": str(location["geoplugin_latitude"]), "lng": str(location["geoplugin_longitude"])}


   return crd


crd = current_location()
print(crd)


# 실행
app = FastAPI()

# 데이터 베이스 연결
redis_pool = redis.ConnectionPool(host='hackathon.kro.kr', port=6379, db=0, max_connections=4, password='onsaemi')

@app.get('/re')
async def receive():
    print("dddsss")


    with redis.StrictRedis(connection_pool=redis_pool) as conn:
        conn.hset('fire_location', 'longitude', '126.77593513491713')
        conn.hset('fire_location', 'latitude', '37.497344670578414')

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)


