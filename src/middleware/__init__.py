from . import auth, cors, errors, alloweds, fernet, blacklist


def register_middleware(app):
    for module in (fernet, auth, cors, errors, alloweds, blacklist):
        module.register(app)
