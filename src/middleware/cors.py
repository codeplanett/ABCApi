from starlette.middleware.cors import CORSMiddleware


CORS_HEADERS = []
CORS_MAX_AGE = 86400
CORS_METHODS = ['DELETE', 'GET', 'PATCH', 'POST', 'PUT']


def add_header(name):
    CORS_HEADERS.append(name)


def register(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='.*',
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
        max_age=CORS_MAX_AGE,
    )
