import jwt
import starlette.requests
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
from starlette.middleware.authentication import AuthenticationMiddleware

from .cors import add_header
from .errors import on_http_error

add_header('Authorization')


class User(BaseUser):
    def __init__(self, data):
        self.username = data['username']
        self.email = data['email']

    @property
    def identity(self):
        raise NotImplementedError

    @property
    def is_authenticated(self):
        return True

    @property
    def name(self):
        return f'{self.username}'

    @property
    def mail(self):
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
    async def authenticate(self, request: starlette.requests.Request):
        if str(request.url).endswith("/register"):
            return None
        try:
            auth: str = request.headers["Authorization"]
            datas = auth.split(" ")
            username = datas[0]
            email = datas[1]
            password = datas[2]
        except KeyError:
            return
        jdata = jwt.encode(payload={"username": username, "email": email}, key=password)
        try:
            dr = await request.app.redis.get(email)
        except:
            raise KatanaAuthError(402, 'The data is incorrect')
        else:
            if dr == jdata:
                return Credentials(jdata), User({"username": username, "email": email})
            else:
                raise KatanaAuthError(402, "The data is incorrect")


def register(app):
    app.add_middleware(AuthenticationMiddleware, backend=KatanaAuthBackend(), on_error=on_http_error)
