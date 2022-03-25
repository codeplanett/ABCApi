import asyncio
import os
import uuid

import yaml
from starlette.authentication import AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class Blacklist:
    def __init__(self, name="./blacklist.yml", **options):
        self.name = name
        self.object_hook = options.pop('object_hook', None)
        self.encoder = options.pop('encoder', None)

        try:
            hook = options.pop('hook')
        except KeyError:
            pass
        else:
            self.object_hook = hook.from_yaml

        self.loop = options.pop('loop', asyncio.get_event_loop())
        self.lock = asyncio.Lock()
        if options.pop('load_later', False):
            self.loop.create_task(self.load())
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.name, 'r') as f:
                self._db = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            self._db = {}

    async def load(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self.load_from_file)

    def _dump(self):
        temp = '%s-%s.tmp' % (uuid.uuid4(), self.name)
        with open(temp, 'w', encoding='utf-8') as tmp:
            yaml.dump(self._db.copy(), tmp, ensure_ascii=True, cls=self.encoder, separators=(',', ':'))
        os.replace(temp, self.name)

    async def save(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

    def get(self, key, *args):
        return self._db.get(str(key), *args)

    async def put(self, key, value, *args):
        self._db[str(key)] = value
        await self.save()

    async def remove(self, key):
        del self._db[str(key)]
        await self.save()

    def __contains__(self, item):
        return str(item) in self._db

    def __getitem__(self, item):
        return self._db[str(item)]

    def __len__(self):
        return len(self._db)

    def all(self):
        return self._db


class KatanaBlacklistError(AuthenticationError):
    def __init__(self, status=401, detail=None):
        self.status_code = status
        self.detail = detail or "I can't brew coffee with a kettle."


class BlacklistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        blacklist = Blacklist()
        await blacklist.load()
        for header in request.headers.raw:
            if header[0] == b'host':
                try:
                    if blacklist.get(header[1].decode("utf-8")):
                        return JSONResponse({"status": "I can't brew coffee with a teapot."}, 418)
                except AttributeError as e:
                    pass
        response = await call_next(request)
        return response


def register(app):
    app.add_middleware(BlacklistMiddleware)
