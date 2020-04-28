from utils import log
from models import Model


def get_salted(password, salt='(。･∀･)ﾉﾞ嗨'):
    from hashlib import sha1
    pw = (password + salt).encode('utf-8')
    return sha1(pw).hexdigest()


class User(Model):
    def __init__(self, d):
        super().__init__(d)
        self.username = d.get('username', '')
        self.password = d.get('password', '')
        self._role = int(d.get('role', 0))
    
    def validate_register(self):
        result = None
        username = self.username
        if len(username) >= 5 and username.isidentifier() and User.find_by(username=username) is None:
            self.password = get_salted(self.password)
            self.add()
            result = self
        return result

    def validate_login(self):
        result = None
        u = User.find_by(username=self.username)
        if u is not None and u.password == get_salted(self.password):
            result = u
        return result

    def is_admin(self):
        return self._role == 1