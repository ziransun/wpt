import random, string, datetime

def id_token():
   letters = string.ascii_lowercase
   return u''.join(random.choice(letters) for i in range(20))

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
      unique_id = id_token()
      headers = [(b"Content-Type", b"text/javascript"),
                 (b"Cache-Control", b"private, max-age=0, stale-while-revalidate=60"),
                 (b"Unique-Id", unique_id.encode("iso-8859-1"))]
      content = u"report('{}')".format(unique_id)
      return 200, headers, content
