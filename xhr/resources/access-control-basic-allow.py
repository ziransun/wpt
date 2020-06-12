#!/usr/bin/env python
def main(request, response):
    response.headers.set(b"Content-Type", b"text/plain")
    response.headers.set(b"Access-Control-Allow-Credentials", b"true")
    response.headers.set(b"Access-Control-Allow-Origin", request.headers.get(b"origin"))

    response.content = u"PASS: Cross-domain access allowed."
