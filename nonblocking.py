from bulbs.rest import *
from pulsar.apps import http
from bulbs.rexster.client import *
from bulbs.gremlin import *
#from bulbs.titan.client import *
#from tornado import gen
import asyncio
#from pulsar import coroutine_return
import traceback,logging
from httplib2 import Response

class Headers(object):
    def __init__(self, headers, status_code):
        self.status_code = status_code

def _process_data(response, **kw):
    if response.status_code == 200:
        data = response.recv_body()
        self.buffer.append(data)

setattr(Request, 'process_data', _process_data)

def _post_request(response):
    logging.warning("post finished"+self.buffer)

setattr(Request, 'post_request', _post_request)

@asyncio.coroutine
def _nb_request(self, method, path, params):
    uri, method, body, headers = self._build_request_args(path, method, params)

    self._display_debug(uri, method, body)

    self.buffer = ''
    http_client = http.HttpClient() #AsyncHTTPClient()
    logging.warning("request: "+method+" "+uri)
    #http_request = http_client.request(method=method,uri,data=body,headers=headers)
    try:
        #response = yield http_client.get('https://github.com/timeline.json')
        res = yield from http_client.request(method,uri,data=body,headers=headers, process_data=self._process_data,post_request=self._post_request)
    except:
        traceback.print_exc()
    try:
        fakeresponse = Response(res.headers)
        fakeresponse.status = res.code
        rc = self.response_class((fakeresponse, self.buffer),self.config)
    except:
        traceback.print_exc()

    return rc

setattr(Request, 'nb_request', _nb_request)
#setattr(Request, 'request', _nb_request)

@asyncio.coroutine
def _nb_get(self, path, params):
    r =  yield from self.nb_request(GET, path, params)
    return r

setattr(Request, 'nb_get', _nb_get)

@asyncio.coroutine
def _nb_put(self, path, params):
    r = yield from self.nb_request(PUT, path, params)
    return r

setattr(Request, 'nb_put', _nb_put)

@asyncio.coroutine
def _nb_post(self, path, params):
    r = yield from self.nb_request(POST, path, params)
    return r

setattr(Request, 'nb_post', _nb_post)

@asyncio.coroutine
def _nb_gremlin(self, script, params=None):
    params = dict(script=script, params=params)
    #if self.config.server_scripts is True:
    #    params["load"] = load or [self.scripts.default_namespace]
    params["load"] = [self.scripts.default_namespace]
    r = yield from self.request.nb_post(gremlin_path, params)
    return r

setattr(RexsterClient, 'nb_gremlin', _nb_gremlin)

@asyncio.coroutine
def _nb_query(self, script, params=None):
    #print ('gremlin!!')
    #print(r)

    resp = yield from self.client.nb_gremlin(script, params)
    #print resp.exception()
    elem = initialize_elements(self.client, resp)
    #raise gen.Return(elem)
    #return elem
    return elem

setattr(Gremlin, 'nb_query', _nb_query)

@asyncio.coroutine
def _nb_execute(self, script, params=None):
    resp = yield from self.client.nb_gremlin(script, params)
    #raise gen.Return(resp)
    return resp

setattr(Gremlin, 'nb_execute', _nb_execute)
