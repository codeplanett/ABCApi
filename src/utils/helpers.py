import datetime
import inspect

from starlette.exceptions import HTTPException


def find_request_parameter(func):
    signature = inspect.signature(func)

    for idx, parameter in enumerate(signature.parameters.values()):
        if parameter.name == 'request':
            return idx

    raise TypeError(f'Unable to locate "request" parameter.')


def parse_expires_at(value):
    if value is None:
        return

    try:
        expires_at = datetime.datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(400, 'Invalid "expires_at" JSON field value.')

    if expires_at > datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10):
        raise HTTPException(400, 'Invalid "expires_at" JSON field value. Must be less than ten years into the future.')

    return expires_at
