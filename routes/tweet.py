from utils import log
from utils import get_env
from utils import template
from utils import make_response_msg
from utils import redirect
from routes.session import require_login
from routes.session import current_user
from models.tweet import Tweet


env = get_env('tweet')


def require_authority(route_func):
    def wrapper(rq):
        tweet_id = int(rq.query.get('id', -1))
        t = Tweet.find(tweet_id)
        user = current_user(rq)
        if t is not None and t.user_id == user.id:
            response_msg = route_func(rq)
        else:
            response_msg = redirect('/login')
        return response_msg
    return wrapper


def index(rq):
    user = current_user(rq)
    if user is None:
        username = '游客'
    else:
        username = user.username
    tweets = Tweet.get_all()
    body = template(env, 'index.html', username=username, tweets=tweets)
    response_msg = make_response_msg(body=body)
    return response_msg


@require_login
def add(rq):
    user = current_user(rq)
    d = rq.form()
    d['user_id'] = user.id
    t = Tweet(d)
    t.add()
    return redirect('/tweet')


# 注意装饰器的顺序
# require_login() 使得登录后才能调用被 require_authority() 装饰的函数
# require_authority() 使得符合权限才能调用 edit()
@require_login
@require_authority
def edit(rq):
    tweet_id = int(rq.query.get('id', -1))
    t = Tweet.find(tweet_id)
    body = template(env, 'edit.html', tweet=t)
    response_msg = make_response_msg(body=body)
    return response_msg


@require_login
@require_authority
def update(rq):
    tweet_id = int(rq.query.get('id', -1))
    t = Tweet.find(tweet_id)
    d = rq.form()
    t.update(d)
    return redirect('/tweet')


@require_login
@require_authority
def delete(rq):
    tweet_id = int(rq.query.get('id', -1))
    t = Tweet.find(tweet_id)
    t.remove()
    return redirect('/tweet')


route_dict = {
    '/tweet': index,
    '/tweet/add': add,
    '/tweet/edit': edit,
    '/tweet/update': update,
    '/tweet/delete': delete,
}