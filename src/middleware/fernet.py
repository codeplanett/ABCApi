import json

import cryptography.fernet
from starlette.authentication import AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils import decrypt_json

from middleware.blacklist import Blacklist


class FernetRequest(Request):
    token = None


class FernetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request = FernetRequest(receive=request.receive, scope=request.scope)
        try:
            try:
                key = request.headers["Authorization"].encode("utf-8")
                auth = decrypt_json(key)
                request.token = json.loads(auth)
            except KeyError as e:
                pass
        except cryptography.fernet.InvalidToken as e:
            blacklist = Blacklist("./blacklist.yml")
            await blacklist.load()
            for header in request.headers.raw:
                if header[0] == b'host':
                    await blacklist.put(header[1].decode("utf-8"), True)
                    await blacklist.save()
                    return JSONResponse({"status": "I can't brew coffee with a teapot."}, 418)
        response = await call_next(request)
        return response


def register(app):
    app.add_middleware(FernetMiddleware)
