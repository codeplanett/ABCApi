import logging

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import *
from src import config


def traces_sampler(sampling_context):
    if "...":
        return 0.5
    elif "...":
        return 0.01
    elif "...":
        return 0
    else:
        return 0.1


sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)


sentry_sdk.init(dsn=str(config.SENTRY),
                integrations=[RedisIntegration(), ExcepthookIntegration(always_run=True), sentry_logging],
                traces_sample_rate=0.2, debug=True, server_name="ABC", release="ABC@1.5.1",
                traces_sampler=traces_sampler)


def register(app):
    app.add_middleware(SentryAsgiMiddleware)
