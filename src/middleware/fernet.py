import json
import logging
import threading
from json import JSONDecodeError

import anyio
import cryptography.fernet
import typing
from starlette.authentication import AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint, DispatchFunction
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.types import ASGIApp, Scope, Receive, Send
from utils import decrypt_json


from middleware.blacklist import Blacklist


class FernetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        blacklist = Blacklist("./blacklist.yml")
        await blacklist.load()
        try:
            try:
                key = request.headers["Authorization"].encode("utf-8")
                auth = decrypt_json(key)
                request.scope["token"] = auth
            except KeyError as e:
                pass
            try:
                data = await request.json()
                data = data["fernetted"].encode()
                json = decrypt_json(data)
                request.scope["json"] = json
            except JSONDecodeError as e:
                pass
        except cryptography.fernet.InvalidToken as e:
            for header in request.headers.raw:
                if header[0] == b'host':
                    await blacklist.put(header[1].decode("utf-8"), True)
                    await blacklist.save()
                    return JSONResponse({"status": "I can't brew coffee with a teapot."}, 418)
        response = await call_next(request)
        return response


def register(app):
    app.add_middleware(FernetMiddleware)
