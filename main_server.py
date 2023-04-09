from aiohttp import web

from LLaMAServer import app

if __name__ == '__main__':
    web.run_app(
        app,
        host='localhost',
        port=8000,
        shutdown_timeout=0.1,
    )
