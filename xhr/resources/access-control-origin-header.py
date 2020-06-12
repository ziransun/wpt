#!/usr/bin/env python
from wptserve.utils import isomorphic_decode

def main(request, response):
    response.headers.set(b"Content-Type", b"text/plain")
    response.headers.set(b"Cache-Control", b"no-cache, no-store")
    response.headers.set(b"Access-Control-Allow-External", b"true")
    response.headers.set(b"Access-Control-Allow-Origin", b"*")

    response.content = u"PASS: Cross-domain access allowed.\n"
    response.content += u"HTTP_ORIGIN: " + isomorphic_decode(request.headers.get(b"origin"))
