import time

def main(request, response):
    code = int(request.GET.first(b"code", 302))
    print(request.url_parts.path)
    location = request.GET.first(b"location", (request.url_parts.path + u"?followed").encode("iso-8859-1")) # ziran

    if b"delay" in request.GET:
        delay = float(request.GET.first(b"delay"))
        time.sleep(delay / 1E3)

    if b"followed" in request.GET:
        return [(b"Content:Type", b"text/plain")], u"MAGIC HAPPENED"
    else:
        return (code, u"WEBSRT MARKETING"), [(b"Location", location)], u"TEST"
