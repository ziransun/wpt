def main(request, response):
    values = request.GET.get_list(b"value")  # ziran - 'latin-1' codec can't encode character '\u20ac' in position 33: ordinal not in range(256)
    content = request.GET.first(b"content", b"<b>hi</b>\n")
    output =  u"HTTP/1.1 200 OK\r\n"
    output += u"X-Content-Type-Options: nosniff\r\n"
    if b"single_header" in request.GET:
        output += u"Content-Type: " + u",".join(values.decode("iso-8859-1")) + u"\r\n"  # convert list values
    else:
        for value in values:
            output += u"Content-Type: " + value.decode("iso-8859-1") + u"\r\n"
    output += u"Content-Length: " + str(len(content)) + u"\r\n"
    output += u"\r\n"
    output += content
    response.writer.write(output)
    response.close_connection = True
