def main(request, response):
    if request.method == u"POST":
        response.add_required_headers = False
        response.writer.write_status(302)
        response.writer.write_header(b"Location", request.url.encode("iso-8859-1"))
        response.writer.end_headers()
        response.writer.write(u"")
    elif request.method == u"GET":
        return ([(b"Content-Type", b"text/plain")],
                u"OK")
    else:
        return ([(b"Content-Type", b"text/plain")],
                u"FAIL")