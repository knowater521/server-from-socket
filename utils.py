# 日志
def log(*args, **kwargs):
    import time
    timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
    print(timestamp)
    print(*args, **kwargs)
    print('<' + '-' * 20)
    print()


# 响应
def make_response_msg(status_code=200, headers={}, body=''):
    '''
    >>> make_response_msg()
    'HTTP/1.1 200 OK\\r\\n\\r\\n'
    >>> make_response_msg(status_code=302, headers={'Location': 'xxx.yyy'})
    'HTTP/1.1 302 Found\\r\\nLocation: xxx.yyy\\r\\n\\r\\n'
    '''
    d = {
        200: 'OK',
        301: 'Moved Permanently',
        302: 'Found',
        404: 'Not Found',
    }
    first_line = f'HTTP/1.1 {str(status_code)} {d[status_code]}\r\n'
    header = ''.join(f'{k}: {v}\r\n' for k, v in headers.items())
    return first_line + header + '\r\n' + body


def redirect(url, headers={}):
    headers['Location'] = url
    return make_response_msg(status_code=302, headers=headers)


# jinja2
def get_env(*path):
    from jinja2 import FileSystemLoader
    from jinja2 import Environment
    import os
    cwd = os.getcwd()
    dirname = os.path.join(cwd, 'templates', *path)
    file_loader = FileSystemLoader(dirname)
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    return env


def template(env, file, *args, **kwargs):
    t = env.get_template(file)
    return t.render(*args, **kwargs)


# json
def save(data, path):
    import json
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, mode='wt', encoding='utf-8') as f:
        f.write(s)


def load(path):
    import json
    with open(path, mode='rt', encoding='utf-8') as f:
        s = f.read()
        data = json.loads(s)
    return data


# session
def make_session_id():
    from uuid import uuid4
    return uuid4().hex


def get_kv(kv):
    '''
    >>> get_kv({'x': 1})
    ('x', 1)
    '''
    for k, v in kv.items():
        key, value = k, v
    return key, value


if __name__ == '__main__':
    import doctest
    doctest.testmod()