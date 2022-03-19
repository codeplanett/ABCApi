import json

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


HANDLERS = []


def add_handler(exception):
    def decorator(func):
        HANDLERS.append((exception, func))
        return func

    return decorator


@add_handler(Exception)
def on_internal_error(request, error):
    return JSONResponse({'error': 'Internal Server Error.'}, 500)


@add_handler(HTTPException)
def on_http_error(request, error):
    stop = '' if error.detail.endswith('.') else '.'
    return JSONResponse({'error': error.detail + stop}, error.status_code)


@add_handler(json.JSONDecodeError)
def on_json_error(request, error):
    return JSONResponse({'error': 'Invalid JSON body.'}, 400)


def register(app):
    for args in HANDLERS:
        app.add_exception_handler(*args)
