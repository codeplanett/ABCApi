import uvicorn.middleware.debug

try:
    import os

    os.chdir("./src")
except FileNotFoundError as e:
    pass

from app import app

config = uvicorn.config.Config(proxy_headers=True, forwarded_allow_ips="*", host="127.0.0.1", port=5005, app=app,
                               debug=True, interface="asgi3", workers=4, server_header=False, date_header=True,
                               use_colors=True)

server = uvicorn.Server(config=config)

if __name__ == '__main__':
    server.run()
