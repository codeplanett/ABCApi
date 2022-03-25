from starlette.responses import JSONResponse
from starlette.routing import Router

from middleware.fernet import FernetRequest

router = Router()


@router.route("/")
async def get_root(request: FernetRequest):
    return JSONResponse({"sign": 'ABC hmmm.'}, 418)
