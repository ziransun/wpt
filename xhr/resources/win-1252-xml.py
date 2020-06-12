def main(request, response):
    headers = [(b"Content-type", b"application/xml;charset=windows-1252")]
    content = u'<' + chr(0xff) + u'/>'   # ziran

    return headers, content
