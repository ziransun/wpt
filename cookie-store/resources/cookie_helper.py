#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Active wptserve handler for cookie operations.
#
# This must support the following requests:
#
# - GET with the following query parameters:
#   - charset: (optional) character set for response (default: utf-8)
#   A cookie: request header (if present) is echoed in the body with a
#   cookie= prefix followed by the urlencoded bytes from the header.
#   Used to inspect the cookie jar from an HTTP request header context.
# - POST with form-data in the body and the following query-or-form parameters:
#   - set-cookie: (optional; repeated) echoed in the set-cookie: response
#     header and also echoed in the body with a set-cookie= prefix
#     followed by the urlencoded bytes from the parameter; multiple occurrences
#     are CRLF-delimited.
#   Used to set cookies from an HTTP response header context.
#
# The response has 200 status and content-type: text/plain; charset=<charset>
import encodings, re

from six import binary_type, PY3

from six.moves.urllib.parse import parse_qs, quote

from wptserve.utils import isomorphic_decode, isomorphic_encode

# NOTE: These are intentionally very lax to permit testing
DISALLOWED_IN_COOKIE_NAME_RE = re.compile(br'[;\0-\x1f\x7f]')
DISALLOWED_IN_HEADER_RE = re.compile(br'[\0-\x1f\x7f]')

# Ensure common charset names do not end up with different
# capitalization or punctuation
CHARSET_OVERRIDES = {
    encodings.codecs.lookup(charset).name: charset
    for charset in (u'utf-8', u'iso-8859-1',)
}

def quote_str(cookie_str):
  if PY3:
    if isinstance(cookie_str, binary_type):
      cookie_str = isomorphic_decode(cookie_str)
    return quote(cookie_str, '', encoding='iso-8859-1')
  else:
    return quote(cookie_str, '')

def parse_qs_str(query_str):
  if PY3:
    if isinstance(query_str, binary_type):
      query_str = isomorphic_decode(query_str)
    return parse_qs(query_str, keep_blank_values=True, encoding='iso-8859-1')
  else:
    return parse_qs(query_str, keep_blank_values=True)

def main(request, response):
  assert request.method in (
      u'GET',
      u'POST',
  ), u'request method was neither GET nor POST: %r' % request.method
  qd = (isomorphic_encode(request.url).split(b'#')[0].split(b'?', 1) + [b''])[1]
  if request.method == u'POST':
    qd += b'&' + request.body
  args = parse_qs_str(qd)

  charset = encodings.codecs.lookup(args.get(u'charset', [u'utf-8'])[-1]).name
  charset = CHARSET_OVERRIDES.get(charset, charset)
  headers = [(b'content-type', b'text/plain; charset=' + isomorphic_encode(charset))]
  body = []
  if request.method == u'POST':
    for set_cookie in args.get('set-cookie', []):
      if '=' in set_cookie.split(';', 1)[0]:
        name, rest = set_cookie.split('=', 1)
        assert re.search(
            DISALLOWED_IN_COOKIE_NAME_RE,
            isomorphic_encode(name)
        ) is None, 'name had disallowed characters: %r' % name
      else:
        rest = set_cookie
      assert re.search(
          DISALLOWED_IN_HEADER_RE,
          isomorphic_encode(rest)
      ) is None, 'rest had disallowed characters: %r' % rest
      headers.append((b'set-cookie', isomorphic_encode(set_cookie)))
      body.append('set-cookie=' + quote_str(set_cookie))

  else:
    cookie = request.headers.get(b'cookie')
    if cookie is not None:
      body.append('cookie=' + quote_str(cookie))
  body = '\r\n'.join(body)
  headers.append((b'content-length', len(body)))
  return 200, headers, body
