from models import Model
from models.user import User
from models.comment import Comment

class Tweet(Model):
    def __init__(self, d):
        super().__init__(d)
        self.content = d.get('content', '')
        self.user_id = int(d.get('user_id', -1))
    
    def user(self):
        user = User.find(self.user_id)
        return user

    def comments(self):
        return Comment.find_all(tweet_id=self.id)
    
    def remove(self):
        comments = self.comments()
        for cmt in comments:
            cmt.remove()
        super().remove()