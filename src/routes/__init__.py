import glob
import glob
import importlib
import sys

from starlette.responses import JSONResponse
from starlette.routing import Mount, Router

from routes import root


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


def load_names(name: str) -> None:
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise Exception(f"Module not found: {name}")
    return _load_from_module_spec(spec, name)


def extract_names():
    names = glob.glob('./routes/*')
    rove = dict()
    returns = []
    for nn in names:
        ver = nn[9:]
        if nn.endswith(".py") or nn.endswith("__pycache__"):
            pass
        else:
            route = load_names(f"routes.{ver}.{ver}")
            rove[ver] = route
    for i in rove:
        routes = getattr(rove[i], "extract_this_version_routes")()
        returns.append(Mount(f"/{i}", routes=routes))
    returns.append(Mount("/", routes=root.router.routes))
    return returns


router = Router(
    extract_names()
)
