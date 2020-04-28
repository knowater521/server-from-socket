from utils import log
from utils import make_response_msg


def error(rq, status_code=404):
    headers = {
        'Content-Type': 'text/html',
    }
    body = '<h3>Not Found</h3>'
    response_msg = make_response_msg(status_code, headers, body)
    return response_msg


def route_func_mapper(path):
    import routes.index
    import routes.session
    import routes.tweet
    import routes.comment
    d = {

    }
    d.update(routes.index.route_dict)
    d.update(routes.session.route_dict)
    d.update(routes.tweet.route_dict)
    d.update(routes.comment.route_dict)
    route_func = d.get(path, error)
    return route_func


def get_response_msg(rq):
    path = rq.path
    route_func = route_func_mapper(path)
    return route_func(rq)


def make_response(connection):
    from parse_request_msg import parse_request_msg
    request_msg = connection.recv(1024).decode('utf-8')
    if len(request_msg) > 0:
        rq = parse_request_msg(request_msg)
        response_msg = get_response_msg(rq)
        connection.sendall(response_msg.encode('utf-8'))
    connection.close()

def run(host, port):
    import socket
    from threading import Thread
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, _ = s.accept()
            t = Thread(target=make_response, args=(connection, ))
            t.start()


if __name__ == '__main__':
    config = dict(
        host='',
        port=2000,
    )
    run(**config)