def main(request, response):
    response.headers.set(b"Content-Type", b"text/html")
    response.headers.set(b"Custom", b"\0")
    return u"<!doctype html><b>This is a document.</b>"
