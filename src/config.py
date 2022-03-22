from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

FERNET_KEY = config('FERNET_KEY', cast=Secret)

REDIS_URL = config('REDIS_URL', cast=Secret)
