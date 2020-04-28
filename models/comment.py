from models import Model
from models.user import User


class Comment(Model):
    def __init__(self, d):
        super().__init__(d)
        self.content = d.get('content', '')
        self.user_id = int(d.get('user_id', -1))
        self.tweet_id = int(d.get('tweet_id', -1))
    
    def user(self):
        user = User.find(self.user_id)
        return user