from . import auth, cors, errors, blocker, sentry


def register_middleware(app):
    for module in (auth, cors, errors, blocker, sentry):
        module.register(app)
