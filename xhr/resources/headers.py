# -*- coding: utf-8 -*-

from wptserve.utils import isomorphic_encode

def main(request, response):
    response.headers.set(b"Content-Type", b"text/plain")
    response.headers.set(b"X-Custom-Header", b"test")
    response.headers.set(b"Set-Cookie", b"test")
    response.headers.set(b"Set-Cookie2", b"test")
    response.headers.set(b"X-Custom-Header-Empty", b"")
    response.headers.set(b"X-Custom-Header-Comma", b"1")
    response.headers.append(b"X-Custom-Header-Comma", b"2")
    response.headers.set(b"X-Custom-Header-Bytes", u"…".encode("utf-8"))
    return u"TEST"
