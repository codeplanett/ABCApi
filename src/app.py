import json
import logging

import aiohttp
import aioredis
from starlette.applications import Starlette

from config import REDIS_URL
from middleware import register_middleware
from routes import router


app = Starlette()

app.redis = None

app.session = None

app.mount('/', router)
register_middleware(app)


@app.on_event('startup')
async def on_startup():
    app.redis = aioredis.Redis.from_url(url=str(REDIS_URL), decode_responses=True)
    logging.debug("ABC On network")

    app.session = aiohttp.ClientSession(headers={'User-Agent': f'ABC/4.0'})


@app.on_event('shutdown')
async def on_shutdown():
    await app.session.close()

    await app.redis.connection_pool.disconnect()
