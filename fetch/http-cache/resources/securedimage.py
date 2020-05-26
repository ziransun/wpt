# -*- coding: utf-8 -

def main(request, response):
    image_url = str.replace(request.url, u"fetch/http-cache/resources/securedimage.py", u"images/green.png")

    if b"authorization" not in request.headers:
        response.status = 401
        response.headers.set(b"WWW-Authenticate", b"Basic")
        return
    else:
        auth = request.headers.get(b"Authorization")
        if auth != b"Basic dGVzdHVzZXI6dGVzdHBhc3M=":
            response.set_error(403, u"Invalid username or password - " + auth.decode("iso-8859-1"))
            return

    response.status = 301
    response.headers.set(b"Location", image_url.encode("iso-8859-1"))
