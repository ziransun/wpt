def main(request, response):
    headers = [(b"Content-type", b"text/html;charset=utf-8")]
    content = u"<!DOCTYPE html><div></div>"

    return headers, content
