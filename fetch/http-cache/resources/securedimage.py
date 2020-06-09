# -*- coding: utf-8 -

from wptserve.utils import isomorphic_decode

def main(request, response):
    image_url = str.replace(request.url, b"fetch/http-cache/resources/securedimage.py", b"images/green.png")

    if b"authorization" not in request.headers:
        response.status = 401
        response.headers.set(b"WWW-Authenticate", b"Basic")
        return
    else:
        auth = request.headers.get(b"Authorization")
        if auth != b"Basic dGVzdHVzZXI6dGVzdHBhc3M=":
            response.set_error(403, u"Invalid username or password - " + isomorphic_decode(auth))
            return

    response.status = 301
    response.headers.set(b"Location", image_url.encode("iso-8859-1"))
