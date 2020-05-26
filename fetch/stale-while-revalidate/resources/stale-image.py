import os.path

def main(request, response):

    token = request.GET.first(b"token", None)
    is_query = request.GET.first(b"query", None) != None
    with request.server.stash.lock:
      value = request.server.stash.take(token)
      count = 0
      if value != None:
        count = int(value)
      if is_query:
        if count < 2:
          request.server.stash.put(token, count)
      else:
        count = count + 1
        request.server.stash.put(token, count)

    if is_query:
      headers = [(b"Count", count)]
      content = u""
      return 200, headers, content
    else:
      filename = u"green-16x16.png"
      if count > 1:
        filename = u"green-256x256.png"

      path = os.path.join(os.path.dirname(__file__), u"../../../images", filename)
      body = open(path, u"rb").read()

      response.add_required_headers = False
      response.writer.write_status(200)
      response.writer.write_header(b"content-length", len(body))
      response.writer.write_header(b"Cache-Control", b"private, max-age=0, stale-while-revalidate=60")
      response.writer.write_header(b"content-type", b"image/png")
      response.writer.end_headers()

      response.writer.write(body)
