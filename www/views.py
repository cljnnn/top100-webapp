import asyncio, aiohttp_jinja2
from aiohttp import web
from storage import update_table
from utils import ConnectionContextManager

@aiohttp_jinja2.template('index.html')
def index(request):
    return {'is_index': True}

@aiohttp_jinja2.template('list.html')
async def db_update(request):
    async with ConnectionContextManager(request.app['db']) as conn:
        query = update_table.select().order_by(update_table.c.id.desc()).limit(20)
        update_list = await conn.execute(query)

    if not update_list:
        raise web.HTTPNotFound()

    return {'update_list': update_list}
