from functools import wraps
import hashlib

from redis.asyncio import Redis

from settings import REDIS_HOST, REDIS_PORT


def cache(expire: int = 30):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = hashlib.md5(f'{func.__name__}:{args}:{kwargs}'.encode()).hexdigest()
            async with Redis(host=REDIS_HOST, port=REDIS_PORT) as redis_session:
                result = await redis_session.get(key)
                if result is None:
                    result = await func(*args, **kwargs)
                    res = str(result.model_dump())
                    await redis_session.set(name=key, value=res, ex=expire)
                    return result
                res = result.decode()
                return eval(res)

        return wrapper

    return decorator
