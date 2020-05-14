import json

from wptserve.utils import isomorphic_encode

def main(request, response):
    response.headers.set(b'Access-Control-Allow-Origin', b'*')
    response.headers.set(b'Access-Control-Allow-Methods', b'OPTIONS, GET, POST')
    response.headers.set(b'Access-Control-Allow-Headers', b'Content-Type')
    response.headers.set(b'Cache-Control', b'no-cache, no-store, must-revalidate');

    # CORS preflight
    if request.method == u'OPTIONS':
        return u''

    uuidMap = {
        b'endpoint': b'01234567-0123-0123-0123-0123456789AB',
        b'report-only-endpoint': b'01234567-0123-0123-0123-0123456789CD'
    }
    key = 0;
    if b'endpoint' in request.GET:
        key = uuidMap[request.GET[b'endpoint']]

    if b'key' in request.GET:
        key = request.GET[b'key']

    if key == 0:
        response.status = 400
        return u'invalid endpoint'

    path = b'/'.join(isomorphic_encode(request.url_parts.path).split(b'/')[:-1]) + b'/'
    if request.method == u'POST':
        reports = request.server.stash.take(key, path) or []
        for report in json.loads(request.body):
            reports.append(report)
        request.server.stash.put(key, reports, path)
        return u'done'

    if request.method == u'GET':
        response.headers.set(b'Content-Type', b'application/json')
        return json.dumps(request.server.stash.take(key, path) or [])

    response.status = 400
    return u'invalid method'
