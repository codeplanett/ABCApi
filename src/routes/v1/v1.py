import routes.v1.account as account
import routes.v1.process as process


def extract_routes(*modules):
    routes = []

    for module in modules:
        routes.extend(module.router.routes)

    return routes


def extract_this_version_routes():
    verroutes = extract_routes(account, process)
    return verroutes
