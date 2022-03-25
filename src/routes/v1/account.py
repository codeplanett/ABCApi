import json
import re

import jwt
import starlette.requests
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.routing import Router

from auth import is_authorized
from middleware import fernet
from utils import decrypt_json

router = Router()


@router.route('/login', methods=['POST'])
@is_authorized
async def katanaLogin(request: fernet.FernetRequest):
    return JSONResponse({"status": "Authorized"})


@router.route('/register', methods=['POST'])
async def katanaRegister(request: fernet.FernetRequest):
    try:
        auth = request.token
        username = auth["username"]
        email = auth["email"]
        password = auth["password"]
    except KeyError:
        return
    try:
        jdata = jwt.encode(payload={"username": username, "email":  email}, key=password)
    except Exception as e:
        raise HTTPException(500, 'There is an error in the JWT encoding')
    try:
        result = await request.app.redis.hset(name=jdata, mapping={"username": username, "email": email})
        resu = await request.app.redis.set(email, str(jdata))
    except Exception as e:
        raise HTTPException(500, f'There is an error in the database Error: {e}')
    if result == 0:
        return JSONResponse({'messages': "Such an account already exists"})
    if result > 0:
        return JSONResponse({'messages': "Account has been created"})
    else:
        return JSONResponse({'messages': "Unexpected database process result"})
