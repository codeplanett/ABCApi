from app import app
import uvicorn

from src.middleware.sentry import sentry_logging

config = uvicorn.config.Config(proxy_headers=True, forwarded_allow_ips="*", host="127.0.0.1", port=5005, app=app,
                               debug=True)
server = uvicorn.Server(config=config)
if __name__ == '__main__':
    server.run()
