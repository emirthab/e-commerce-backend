import redis.asyncio as aioredis

from config import config

redis = aioredis.from_url(url=f"redis://{config.REDIS_HOST}:{str(config.REDIS_PORT)}", username=config.REDIS_USER, password=config.REDIS_PASSWORD)