import json

def main(request, response):
    key = request.GET.first(b"stash")
    origin = request.headers.get(b"origin")
    if origin is None:
        origin = b"no Origin header"

    origin_list = request.server.stash.take(key)

    if b"dump" in request.GET:
        response.headers.set(b"Content-Type", b"application/json")
        response.content = json.dumps(origin_list)
        return

    if origin_list is None:
        origin_list = [origin.decode("iso-8859-1")]
    else:
        origin_list.append(origin.decode("iso-8859-1"))

    request.server.stash.put(key, origin_list)

    if b"location" in request.GET:
        response.status = 308
        response.headers.set(b"Location", request.GET.first(b"location"))
        return

    response.headers.set(b"Content-Type", b"text/html")
    response.headers.set(b"Access-Control-Allow-Origin", b"*")
    response.content = u"<meta charset=utf-8>\n<body><script>parent.postMessage('loaded','*')</script></body>"
