def main(request, response):
    headers = [(b"Content-Encoding", b"gzip")]
    return headers, u"not actually gzip"
