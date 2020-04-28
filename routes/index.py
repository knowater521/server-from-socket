from utils import log
from utils import get_env
from utils import template
from utils import make_response_msg
from routes.session import current_user


env = get_env()


def index(rq):
    user = current_user(rq)
    if user is None:
        username = '游客'
    else:
        username = user.username
    body = template(env, 'index.html', username=username)
    response_msg = make_response_msg(body=body)
    return response_msg


route_dict = {
    '/': index,
}