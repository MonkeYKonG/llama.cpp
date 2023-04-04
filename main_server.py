from aiohttp import web

from LLaMAServer import app

web.run_app(
    app,
    host='localhost',
    port='8000',
)