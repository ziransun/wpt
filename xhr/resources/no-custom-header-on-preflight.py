def main(request, response):
    def getState(token):
        server_state = request.server.stash.take(token)
        if not server_state:
            return b"Uninitialized"
        return server_state

    def setState(state, token):
        request.server.stash.put(token, state)

    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Access-Control-Allow-Headers", "x-test")
    response.headers.set("Access-Control-Max-Age", 0)
    token = request.GET.first("token", None)

    if request.method == u"OPTIONS":
        if request.headers.get(b"x-test"):
            response.content = u"FAIL: Invalid header in preflight request."
            response.status = 400
        else:
            setState(b"PASS", token)
    else:
        if request.headers.get(b"x-test"):
            response.content = getState(token)
        else:
            response.content = u"FAIL: X-Test header missing in request"
            response.status = 400
