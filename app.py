#!/usr/bin/env python3
"""Example for aiohttp.web websocket server
"""

import asyncio
import os,json
from aiohttp.web import Application, Response, MsgType, WebSocketResponse
from aiohttp_session import get_session #, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import jinja2
import asyncio_redis
#WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')

"""
response_id = 0
def gen_block_id(response, msg):
    global response_id
    if 'block_id' in msg and msg['block_id']:
        print('returning duplicate blockid',msg['block_id'])
        my_id = msg['block_id']
    else:
        print('generating new blockid')
        my_id = 'mbe' + str(response_id)
        response_id += 1
    return '<div class="mbe" id="' + my_id + '">\r\n' + response + '\r\n</div>\r\n'
"""

def wshandler_login(ws, request, msg):
    kwds = msg["data"].split()
    if len(kwds) > 1:
        ws.send_str(json.dumps({'eventName': 'inject', 'data': '<div style="border:4px solid green;">login user: ' + kwds[1] + " pass: " + kwds[2] + '</div>'}))
    else:
        response = aiohttp_jinja2.render_template('login.jinja2', request, {})
        response_text = response.text
        ws.send_str(json.dumps({'eventName': 'inject', 'data': response_text}))

def wshandler_test(ws, request, msg):
        ws.send_str(json.dumps({'eventName': 'inject', 'data': '<div>BLOCK TEST</div>'}))

class WebsocketHandler:
    def __init__(self):
        pass

    @asyncio.coroutine
    def handle(self, request):
        self.request = request
        ws = WebSocketResponse()
        ws.start(request)

        connection = yield from asyncio_redis.Connection.create(host='127.0.0.1', port=6379)
        subscriber = yield from connection.start_subscribe()
        yield from subscriber.subscribe(['ch1', 'ch2'])

        print('Connection opened')
        try:
            # Kick off both coroutines in parallel, and then block
            # until both are completed.
            yield from asyncio.gather(self.handle_ws(ws), self.handle_redis(subscriber))
            #yield from self.handle_ws(ws)
        except Exception as e:  # Don't do except: pass
            import traceback
            traceback.print_exc()
        finally:
            print('Connection closed')
        return ws

    @asyncio.coroutine
    def handle_ws(self, ws):
        while True:
            msg_ws = yield from ws.receive()
            if msg_ws:
                yield from self.on_msg_from_ws(ws, msg_ws)

    @asyncio.coroutine
    def handle_redis(self, subscriber):
        while True:
            msg_redis = yield from subscriber.next_published()
            if msg_redis:
                yield from self.on_msg_from_redis(redis, msg_redis)

    @asyncio.coroutine
    def on_msg_from_ws(self, ws, msg):
        msg = json.loads(msg.data)
        print(msg)
        if msg["eventName"] == 'cmd':
            if msg["data"].startswith('login'):
                wshandler_login(ws, self.request, msg)
            elif msg["data"].startswith('test'):
                wshandler_test(ws, self.request, msg)
        #yield from (msg.data)
        #yield from connection.publish('our-channel', text)

    @asyncio.coroutine
    def on_msg_from_redis(self, redis, msg):
        print(msg)

@asyncio.coroutine
def home(request):
    response = aiohttp_jinja2.render_template('home.jinja2', request, {})
    response.headers['Content-Language'] = 'en'
    return response


@asyncio.coroutine
def init(loop):
    app = Application(loop=loop)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app['sockets'] = []
    app.router.add_static('/static', 'static')
    app.router.add_route('GET', '/', home)
    wshandler = WebsocketHandler()
    app.router.add_route('GET', '/ws', wshandler.handle)

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return app, srv, handler


@asyncio.coroutine
def finish(app, srv, handler):
    for ws in app['sockets']:
        ws.close()
    app['sockets'].clear()
    yield from asyncio.sleep(0.1)
    srv.close()
    yield from handler.finish_connections()
    yield from srv.wait_closed()


loop = asyncio.get_event_loop()
app, srv, handler = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(finish(app, srv, handler))
