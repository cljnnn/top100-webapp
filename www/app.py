import logging; logging.basicConfig(level=logging.INFO)

import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
from aiomysql.sa import create_engine
from config import configs
import views

async def db_middleware(app, handler):
    async def middleware(request):
        db = app.get('db')
        if not db:
            config = app.get('dsn')
            app['db'] = db = await create_engine(**config)
        request.app['db'] = db
        return await handler(request)
    return middleware

app = web.Application(middlewares=[db_middleware])
app['dsn'] = configs.db
app.router.add_route('GET', '/', views.index)
app.router.add_route('GET', '/list', views.db_update)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))

if __name__ == '__main__':
    async def init(loop):
        srv = await loop.create_server(app.make_handler(), '0.0.0.0', 8800)
        logging.info('server started at port 8800...')
        return srv

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
