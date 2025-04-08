import redis


def get_redis_client() -> redis.Redis:
    r = redis.Redis(host="redis", port=6379, decode_responses=True, password="mypass")
    return r
