def main(request, response):
    if request.method == u"OPTIONS":
        response.headers.set(b"Content-Type", b"text/plain")
        response.headers.set(b"Access-Control-Allow-Credentials", b"true")
        response.headers.set(b"Access-Control-Allow-Methods", b"PUT")
        response.headers.set(b"Access-Control-Allow-Origin", request.headers.get(b"origin"))

    elif request.method == u"PUT":
        response.headers.set(b"Content-Type", b"text/plain")
        response.headers.set(b"Access-Control-Allow-Credentials", b"true")
        response.headers.set(b"Access-Control-Allow-Origin", request.headers.get(b"origin"))
        response.content = u"PASS: Cross-domain access allowed."
        try:
            response.content += u"\n" + request.body   # ziran: request.body type
        except:
            response.content += u"Could not read in content."

    else:
        response.headers.set(b"Content-Type", b"text/plain")
        response.content = u"Wrong method: " + request.method
