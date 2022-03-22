import asyncio
import glob
import importlib
import logging
import sys

from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, Router

from src.routes.v1 import process, account


def get_root(request):
    return PlainTextResponse('ABC hmmm.')


def extract_routes(*modules):
    routes = []

    for module in modules:
        routes.extend(module.router.routes)

    return routes


def _load_from_module_spec(spec: importlib.machinery.ModuleSpec, key: str) -> None:
    lib = importlib.util.module_from_spec(spec)
    sys.modules[key] = lib
    try:
        spec.loader.exec_module(lib)
    except Exception as e:
        del sys.modules[key]
        raise Exception(key, e) from e
    try:
        setup = getattr(lib, 'extract_this_version_routes')
    except AttributeError:
        del sys.modules[key]
        raise Exception("No Entry Point Erro: " + key)
    else:
        return lib


def load_version(name: str) -> None:
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise Exception(f"Module not found: {name}")
    return _load_from_module_spec(spec, name)


def extract_versions():
    names = glob.glob('./routes/*')
    rove = dict()
    returns = []
    for nn in names:
        ver = nn[9:]
        if nn.endswith(".py") or nn.endswith("__pycache__"):
            pass
        else:
            route = load_version(f"routes.{ver}.{ver}")
            rove[ver] = route
    for i in rove:
        routes = getattr(rove[i], "extract_this_version_routes")()
        returns.append(Mount(f"/{i}", routes=routes))
    return returns


router = Router(
    extract_versions()
)
