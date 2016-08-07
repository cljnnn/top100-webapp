import asyncio, aiohttp_jinja2
from aiohttp import web
from storage import update_table

@aiohttp_jinja2.template('index.html')
def index(request):
    return {'is_index': True}

@aiohttp_jinja2.template('list.html')
def db_update(request):
    with (yield from request.app['db']) as conn:
        query = update_table.select()
        update_list = yield from conn.execute(query)

    if not update_list:
        raise web.HTTPNotFound()

    return {'update_list': update_list}