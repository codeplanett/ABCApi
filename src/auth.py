import functools

from starlette.exceptions import HTTPException

from utils import find_request_parameter


def is_authorized(func):
    idx = find_request_parameter(func)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request', args[idx])

        if not request.user.is_authenticated:
            raise HTTPException(401, 'Authorization required.')

        return await func(*args, **kwargs)

    return wrapper
