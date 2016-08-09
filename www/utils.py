import ujson

from aiohttp import web
import decimal, datetime

class ConnectionContextManager(object):

    def __init__(self, engine):
        self.conn = None
        self.engine = engine

    async def __aenter__(self):
        self.conn = await self.engine.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        try:
            self.engine.release(self.conn)
        finally:
            self.conn = None
            self.engine = None

def _alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    
def json_response(data, **kwargs):
    # Sometimes user needs to override default content type for JSON
    kwargs.setdefault('content_type', 'application/json')
    body=ujson.dumps([dict(r) for r in data])
    return web.Response(body=body.encode('utf8'), **kwargs)
