def main(request, response):
    time = request.url_parts.query if request.url_parts.query else b'0'
    return 200, [(b'Refresh', time), (b'Content-Type', b"text/html")], u''
