import redis
from django.conf import settings

_redis = None


def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


def block_token(jti: str, exp_timestamp: int):
    import time

    ttl = int(exp_timestamp - time.time())
    if ttl <= 0:
        ttl = 1
    r = get_redis()
    r.setex(f"blacklist_jti:{jti}", ttl, "1")


def is_token_blocked(jti: str) -> bool:
    r = get_redis()
    return r.exists(f"blacklist_jti:{jti}") == 1
