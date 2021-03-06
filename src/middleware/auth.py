import json
from abc import ABC, abstractmethod

import jwt
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from utils import decrypt_json

from . import fernet
from .cors import add_header
from .errors import on_http_error

add_header('Authorization')


class User(BaseUser, ABC):
    def __init__(self, data):
        self.username = data['username']
        self.mail = data['email']
        self.token = data["token"]

    @property
    def identity(self):
        return f"{self.token}"

    @property
    def is_authenticated(self):
        return True

    @property
    def name(self):
        return f'{self.username}'

    @property
    def email(self):
        return f'{self.email}'


class Credentials(AuthCredentials):
    def __init__(self, token):
        super().__init__()
        self.token = token


class KatanaAuthError(AuthenticationError):
    def __init__(self, status=401, detail=None):
        self.status_code = status
        self.detail = detail or 'Authorization failed.'


class KatanaAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: HTTPConnection):
        if str(request.url).endswith("/register"):
            return None
        try:
            key = request.headers["Authorization"].encode("utf-8")
            auth = decrypt_json(key)
            username = auth["username"]
            email = auth["email"]
            password = auth["password"]
        except KeyError:
            return
        jdata = jwt.encode(payload={"username": username, "email": email}, key=password)
        try:
            dr = await request.app.redis.get(email)
        except:
            raise KatanaAuthError(402, 'The data is incorrect')
        else:
            if dr == jdata:
                return Credentials(jdata), User({"username": username, "email": email, "token": jdata})
            else:
                raise KatanaAuthError(402, "The data is incorrect")


def register(app):
    app.add_middleware(AuthenticationMiddleware, backend=KatanaAuthBackend(), on_error=on_http_error)
