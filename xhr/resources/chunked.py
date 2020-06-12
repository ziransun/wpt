def main(request, response):
    chunks = [u"First chunk\r\n",
              u"Second chunk\r\n",
              u"Yet another (third) chunk\r\n",
              u"Yet another (fourth) chunk\r\n",
              ]
    response.headers.set(b"Transfer-Encoding", b"chunked")
    response.headers.set(b"Trailer", b"X-Test-Me")
    response.headers.set(b"Content-Type", b"text/plain")
    response.write_status_headers()

    for value in chunks:
        response.writer.write(u"%x\r\n" % len(value))
        response.writer.write(value)
        response.writer.write(u"\r\n")
    response.writer.write(u"0\r\n")
    response.writer.write(u"X-Test-Me: Trailer header value\r\n\r\n")
