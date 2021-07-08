import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book_info = DB.title_info(book_id)
    if book_info is None:
        raise NameError

    response_body = ("<html><body>"
                     f"<h1>{book_info['title']}</h1>"
                     "<table>"
                     f"<tr><th>Author:</th><td>{book_info['author']}</td></tr>"
                     f"<tr><th>Publisher:</th><td>{book_info['publisher']}</td></tr>"
                     f"<tr><th>ISBN:</th><td>{book_info['isbn']}</td></tr>"
                     "</table>"
                     "<a href=\"/\">Back to the list</a>"
                     "</body></html>"
                     )
    return response_body


def books():
    book_list = DB.titles()
    response_body = "<html><body><h1>My Bookshelf</h1><ul>"
    for book in book_list:
        response_body += f"<li><a href=\"/book/{book['id']}\">{book['title']}</a></li>"
    response_body += "</ul></body></html>"
    return response_body


def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    request_uri = environ.get("PATH_INFO", None)
    if request_uri is None:
        status = "404 Not Found"
        body = "Page not found."

    request_path = request_uri.strip('/').split('/')
    handler = request_path[0]
    params = request_path[1:]

    if handler == '':
        body = books()
    elif handler == 'book':
        try:
            body = book(params[0])
        except NameError:
            status = "404 Not Found"
            body = "Book not found in database."
        except Exception:
            status = "500 Internal Server Error"
            body = "Internal server error."
    else:
        status = "404 Not Found"
        body = "Page not found."

    headers.append(('Content-length', str(len(body))))
    start_response(status, headers)
    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
