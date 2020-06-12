from wptserve.utils import isomorphic_decode

def main(request, response):
    content = []

    print(request.POST.items())
    for key, values in sorted(item for item in request.POST.items() if not hasattr(item[1][0], u"filename")):
        content.append(u"%s=%s," % (isomorphic_decode(key), values[0]))
    content.append(u"\n")

    for key, values in sorted(item for item in request.POST.items() if hasattr(item[1][0], u"filename")):
        value = values[0]
        content.append(u"%s=%s:%s:%s," % (isomorphic_decode(key),
                                         value.filename,
                                         value.headers[u"Content-Type"],
                                         len(value.file.read())))

    return u"".join(content)
