from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Router

router = Router()


@router.route("/")
async def get_root(request: Request):
    return JSONResponse({"sign": 'ABC hmmm.'}, 418)
