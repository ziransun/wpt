from six import ensure_str

def main(request, response):
    headers = []
    if "cors" in request.GET:
        headers.append(("Access-Control-Allow-Origin", "*"))
        headers.append(("Access-Control-Allow-Credentials", "true"))
        headers.append(("Access-Control-Allow-Methods", "GET, POST, PUT, FOO"))
        headers.append(("Access-Control-Allow-Headers", "x-test, x-foo"))
        headers.append(("Access-Control-Expose-Headers", "x-request-method"))

    headers.append(("x-request-method", request.method))
    headers.append(("x-request-content-type",
                    ensure_str(request.headers.get("Content-Type", "NO"))))
    headers.append(("x-request-content-length", 
                    ensure_str(request.headers.get("Content-Length", "NO"))))
    headers.append(("x-request-content-encoding",
                    ensure_str(request.headers.get("Content-Encoding", "NO"))))
    headers.append(("x-request-content-language", request.headers.get("Content-Language", b"NO").decode("utf-8")))
    headers.append(("x-request-content-location", request.headers.get("Content-Location", b"NO").decode("utf-8")))
    return headers, request.body
