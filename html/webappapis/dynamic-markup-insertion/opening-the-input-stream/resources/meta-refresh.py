from wptserve.utils import isomorphic_decode

def main(request, response):
    time = request.url_parts.query if request.url_parts.query else b'0'
    return 200, [[b'Content-Type', b'text/html']], u'<meta http-equiv=refresh content=%s>' % isomorphic_decode(time)
