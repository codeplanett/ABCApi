from starlette.middleware.trustedhost import TrustedHostMiddleware


def register(app):
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1"])
