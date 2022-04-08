import re

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Router

from auth import is_authorized

router = Router()


@router.route("/set", methods=['POST'])
@is_authorized
async def set(request: Request):
    try:
        data: dict = request.scope["json"]
        key = data["name"]
        data.pop("name")
        data["identity"] = request.user.identity
    except:
        return JSONResponse({"status": "We were unable to provide the required data."}, 400)
    try:
        await request.app.redis.hset(key, mapping=data)
    except Exception as e:
        return JSONResponse({"status": "Your data could not be saved or modified in the database."})
    else:
        return JSONResponse({"status": "Data has been saved"})


@router.route("/get", methods=['POST'])
@is_authorized
async def get(request: Request):
    data = request.scope["json"]
    key = data["name"]
    try:
        dbResult = await request.app.redis.hgetall(key)
    except:
        return JSONResponse({"status": "Data could not be getted for an unknown reason."})
    if dbResult["identity"] == request.user.identity:
        return JSONResponse(dbResult)
    else:
        return JSONResponse({"status": "You not get this data."})
