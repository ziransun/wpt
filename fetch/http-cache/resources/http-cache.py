#!/usr/bin/env python

import datetime
import json
import time
from base64 import b64decode

from wptserve.utils import isomorphic_decode, isomorphic_encode

NOTEHDRS = set([b'content-type', b'access-control-allow-origin', b'last-modified', b'etag'])
NOBODYSTATUS = set([204, 304])
LOCATIONHDRS = set([b'location', b'content-location'])
DATEHDRS = set([b'date', b'expires', b'last-modified'])

def main(request, response):
    dispatch = request.GET.first(b"dispatch", None)
    uuid = request.GET.first(b"uuid", None)

    if request.method == u"OPTIONS":
        return handle_preflight(uuid, request, response)
    if not uuid:
        response.status = (404, b"Not Found")
        response.headers.set(b"Content-Type", b"text/plain")
        return b"UUID not found"
    if dispatch == b'test':
        return handle_test(uuid, request, response)
    elif dispatch == b'state':
        return handle_state(uuid, request, response)
    response.status = (404, b"Not Found")
    response.headers.set(b"Content-Type", b"text/plain")
    return b"Fallthrough"

def handle_preflight(uuid, request, response):
    response.status = (200, b"OK")
    response.headers.set(b"Access-Control-Allow-Origin", b"*")
    response.headers.set(b"Access-Control-Allow-Methods", b"GET")
    response.headers.set(b"Access-Control-Allow-Headers", b"*")
    response.headers.set(b"Access-Control-Max-Age", b"86400")
    return b"Preflight request"

def handle_state(uuid, request, response):
    response.headers.set(b"Content-Type", b"text/plain")
    return json.dumps(isomorphic_decode(request.server.stash.take(uuid)))

def handle_test(uuid, request, response):
    server_state = request.server.stash.take(uuid) or []
    try:
        requests = json.loads(b64decode(request.headers.get(b'Test-Requests', b"")))
    except:
        response.status = (400, b"Bad Request")
        response.headers.set(b"Content-Type", b"text/plain")
        return b"No or bad Test-Requests request header"
    config = requests[len(server_state)]
    if not config:
        response.status = (404, b"Not Found")
        response.headers.set(b"Content-Type", b"text/plain")
        return b"Config not found"
    noted_headers = {}
    now = time.time()
    for header in config.get(b'response_headers', []):
        if header[0].lower() in LOCATIONHDRS: # magic locations
            if (len(header[1]) > 0):
                header[1] = b"%s&target=%s" % (isomorphic_encode(request.url), header[1])
            else:
                header[1] = isomorphic_encode(request.url)
        if header[0].lower() in DATEHDRS and isinstance(header[1], int):  # magic dates
            header[1] = http_date(now, header[1])
        response.headers.set(header[0], header[1])
        if header[0].lower() in NOTEHDRS:
            noted_headers[header[0].lower()] = header[1]
    state = {
        b'now': now,
        b'request_method': request.method,
        b'request_headers': dict([[h.lower(), request.headers[h]] for h in request.headers]),
        b'response_headers': noted_headers
    }
    server_state.append(state)
    request.server.stash.put(uuid, server_state)

    if b"access-control-allow-origin" not in noted_headers:
        response.headers.set(b"Access-Control-Allow-Origin", b"*")
    if b"content-type" not in noted_headers:
        response.headers.set(b"Content-Type", b"text/plain")
    response.headers.set(b"Server-Request-Count", len(server_state))

    code, phrase = config.get(b"response_status", [200, b"OK"])
    if config.get(b"expected_type", b"").endswith(b'validated'):
        ref_hdrs = server_state[0][b'response_headers']
        previous_lm = ref_hdrs.get(b'last-modified', False)
        if previous_lm and request.headers.get(b"If-Modified-Since", False) == isomorphic_encode(previous_lm):
            code, phrase = [304, b"Not Modified"]
        previous_etag = ref_hdrs.get(b'etag', False)
        if previous_etag and request.headers.get(b"If-None-Match", False) == isomorphic_encode(previous_etag):
            code, phrase = [304, b"Not Modified"]
        if code != 304:
            code, phrase = [999, b'304 Not Generated']
    response.status = (code, phrase)

    content = config.get(b"response_body", uuid)
    if code in NOBODYSTATUS:
        return b""
    return content


def get_header(headers, header_name):
    result = None
    for header in headers:
        if header[0].lower() == header_name.lower():
            result = header[1]
    return result

WEEKDAYS = [b'Mon', b'Tue', b'Wed', b'Thu', b'Fri', b'Sat', b'Sun']
MONTHS = [None, b'Jan', b'Feb', b'Mar', b'Apr', b'May', b'Jun', b'Jul',
          b'Aug', b'Sep', b'Oct', b'Nov', b'Dec']

def http_date(now, delta_secs=0):
    date = datetime.datetime.utcfromtimestamp(now + delta_secs)
    return b"%s, %.2d %s %.4d %.2d:%.2d:%.2d GMT" % (
        WEEKDAYS[date.weekday()],
        date.day,
        MONTHS[date.month],
        date.year,
        date.hour,
        date.minute,
        date.second)
