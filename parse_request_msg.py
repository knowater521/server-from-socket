from utils import log


def parse_kvs(kvs, sep, eq):
    '''
    >>> parse_kvs('a=1&b=2', sep='&', eq='=')
    {'a': '1', 'b': '2'}
    >>> parse_kvs('', sep='&', eq='=')
    {}
    >>> parse_kvs('a=&b=', sep='&', eq='=')
    {'a': '', 'b': ''}
    '''
    d = {}
    if kvs != '':
        for kv in kvs.split(sep):
            k, v = kv.split(eq, 1)
            d[k] = v
    return d


def parse_kvs_with_unquote(kvs, sep, eq):
    '''
    >>> parse_kvs_with_unquote('a%20=%20b', sep='&', eq='=')
    {'a ': ' b'}
    '''
    from urllib.parse import unquote
    d = {}
    if kvs != '':
        for kv in kvs.split(sep):
            k, v = kv.split(eq, 1)
            k = unquote(k)
            v = unquote(v)
            d[k] = v
    return d


def parse_path_query(path_query):
    '''
    >>> parse_path_query('/?a%20=%20b')
    ('/', {'a ': ' b'})
    >>> parse_path_query('/')
    ('/', {})
    '''
    if '?' in path_query:
        path, query = path_query.split('?', 1)
        query = parse_kvs_with_unquote(query, sep='&', eq='=')
    else:
        path = path_query
        query = {}
    return path, query


def parse_header(header):
    '''
    >>> parse_header('Location: xxx.yyy\\r\\nContent-Type: text/html')
    {'Location': 'xxx.yyy', 'Content-Type': 'text/html'}
    >>> parse_header('')
    {}
    '''
    headers = parse_kvs(header, sep='\r\n', eq=': ')
    return headers


class Request:
    def __init__(self, method, path, query, headers, body):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
    
    def form(self):
        # return parse_kvs_with_unquote(self.body, sep='&', eq='=')
        return parse_kvs(self.body, sep='&', eq='=')
    
    def cookie(self):
        cookie = {}
        if 'Cookie' in self.headers.keys():
            kvs = self.headers['Cookie']
            # cookie: VISITOR_INFO1_LIVE=Ic28Su7wG2k; PREF=f40;
            cookie = parse_kvs(kvs, sep='; ', eq='=')
        return cookie


def parse_request_msg(request_msg:str):
    head, body = request_msg.split('\r\n\r\n', 1)
    first_line, header = head.split('\r\n', 1)
    method, path_query, _ = first_line.split()
    path, query = parse_path_query(path_query)
    headers = parse_header(header)
    return Request(method, path, query, headers, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod()


