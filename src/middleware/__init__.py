from . import auth, cors, errors, blocker, fernet, blacklist


def register_middleware(app):
    for module in (fernet, auth, cors, errors, blocker, blacklist):
        module.register(app)
