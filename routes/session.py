from utils import log
from utils import get_env
from utils import template
from utils import make_response_msg
from utils import redirect
from utils import make_session_id
from models.user import User


session = {}
env = get_env('session')


def current_user(rq):
    user = None
    session_id = rq.cookie().get('session_id', '')
    if session_id != '' and session != {}:
        user_id = session[session_id]
        user = User.find(user_id)
    return user


def require_login(route_func):
    def wrapper(rq):
        log('require_login')
        user = current_user(rq)
        if user is None:
            response_msg = redirect('/login')
        else:
            response_msg = route_func(rq)
        return response_msg
    return wrapper


def register(rq):
    if rq.method == 'POST':
        d = rq.form()
        user = User(d)
        if user.validate_register() is not None:
            response_msg = redirect('/login')
        else:
            response_msg = redirect('/register')
    else:
        body = template(env, 'register.html')
        response_msg = make_response_msg(body=body)
    return response_msg


def login(rq):
    if rq.method == 'POST':
        d = rq.form()
        user = User(d)
        if (u := user.validate_login()) is not None:
            session_id = make_session_id()
            session[session_id] = u.id
            headers = {
                'Set-Cookie': f'session_id={session_id}',
            }
            response_msg = redirect('/', headers)
            log('登录成功')
        else:
            response_msg = redirect('/login')
            log('账号或密码错误')
    else:
        body = template(env, 'login.html')
        response_msg = make_response_msg(body=body)
    return response_msg


route_dict = {
    '/register': register,
    '/login': login,
}