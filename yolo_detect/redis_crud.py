import redis


redis_pool = redis.ConnectionPool(host='hackathon.kro.kr', port=6379, db=0, max_connections=4, password='onsaemi')

with redis.StrictRedis(connection_pool=redis_pool) as conn:
    conn.hset('fire_detect', 'fire_outbreak', 'on')
    conn.hset('fire_detect', 'latitue', '36.5000')
    conn.hset('fire_detect', 'longitude', '127.123')

    outbreak = conn.hget('fire_detect', 'fire_outbreak').decode('utf-8')
    latitude = conn.hget('fire_detect', 'latitue').decode('utf-8')
    longitude = conn.hget('fire_detect', 'longitude').decode('utf-8')

print(outbreak, latitude, longitude)