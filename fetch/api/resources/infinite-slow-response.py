import time

from wptserve.utils import isomorphic_decode

def url_dir(request):
    return u'/'.join(request.url_parts.path.split(u'/')[:-1]) + u'/'


def stash_write(request, key, value):
    """Write to the stash, overwriting any previous value"""
    print(key)
    request.server.stash.take(key, url_dir(request))
    print(value)
    print(type(value))
    request.server.stash.put(key, value, url_dir(request))   # value -> string or bytes?


def main(request, response):
    stateKey = isomorphic_decode(request.GET.first(b"stateKey", b""))
    abortKey = isomorphic_decode(request.GET.first(b"abortKey", b""))

    if stateKey:
        stash_write(request, stateKey, u'open')

    response.headers.set(b"Content-type", b"text/plain")
    response.write_status_headers()

    # Writing an initial 2k so browsers realise it's there. *shrug*
    response.writer.write(u"." * 2048)

    while True:
        if not response.writer.flush():
            break
        if abortKey and request.server.stash.take(abortKey, url_dir(request)):
            break
        response.writer.write(u".")
        time.sleep(0.01)

    if stateKey:
        stash_write(request, stateKey, u'closed')   # ziran - bytes string? write?
