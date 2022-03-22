from . import auth, cors, errors, blocker


def register_middleware(app):
    for module in (auth, cors, errors, blocker):
        module.register(app)
