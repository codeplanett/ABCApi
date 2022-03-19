from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, Router

from . import (gettings, account)


def get_root(request):
    return PlainTextResponse('ABC hmmm.')


def extract_routes(*modules):
    routes = []

    for module in modules:
        routes.extend(module.router.routes)

    return routes


router = Router(
    [
        Route('/', get_root),
        Mount(
            '/v1',
            routes=extract_routes(gettings, account),
        ),
    ]
)
