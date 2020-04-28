from utils import log
from utils import get_env
from utils import template
from utils import make_response_msg
from utils import redirect
from routes.session import require_login
from routes.session import current_user
from models.tweet import Comment


env = get_env('comment')


def require_authority(route_func):
    def wrapper(rq):
        cmt_id = int(rq.query.get('id', -1))
        cmt = Comment.find(cmt_id)
        user = current_user(rq)
        if cmt is not None and cmt.user_id == user.id:
            response_msg = route_func(rq)
        else:
            response_msg = redirect('/login')
        return response_msg
    return wrapper


@require_login
def add(rq):
    user = current_user(rq)
    d = rq.form()
    d['tweet_id'] = int(rq.query['id'])
    d['user_id'] = user.id
    t = Comment(d)
    t.add()
    return redirect('/tweet')


@require_login
@require_authority
def edit(rq):
    cmt_id = int(rq.query.get('id', -1))
    cmt = Comment.find(cmt_id)
    body = template(env, 'edit.html', comment=cmt)
    response_msg = make_response_msg(body=body)
    return response_msg


@require_login
@require_authority
def update(rq):
    cmt_id = int(rq.query.get('id', -1))
    cmt = Comment.find(cmt_id)
    d = rq.form()
    cmt.update(d)
    return redirect('/tweet')


@require_login
@require_authority
def delete(rq):
    cmt_id = int(rq.query.get('id', -1))
    cmt = Comment.find(cmt_id)
    cmt.remove()
    return redirect('/tweet')


route_dict = {
    '/comment/add': add,
    '/comment/edit': edit,
    '/comment/update': update,
    '/comment/delete': delete,
}