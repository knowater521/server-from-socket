import os
import time
from utils import log
from utils import save
from utils import load
from utils import get_kv


def formatted_time(secs, fmt):
    time_struct = time.localtime(secs)
    time_stamp = time.strftime(fmt, time_struct)
    return time_stamp


class Model:
    @classmethod
    def db_path(cls):
        import os
        cwd = os.getcwd()
        dirname = os.path.join(cwd, 'db')
        filename = f'{cls.__name__}.txt'
        return os.path.join(dirname, filename)

    @classmethod
    def get_all(cls):
        path = cls.db_path()
        data = load(path)
        models = [cls(d) for d in data]
        return models

    @classmethod
    def find_by(cls, **kwargs):
        k, v = get_kv(kwargs)
        models = cls.get_all()
        result = None
        for m in models:
            try:
                val = m.__dict__[k]
            except KeyError:
                pass
            else:
                if val == v:
                    result = m
                    break
        return result

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        k, v = get_kv(kwargs)
        models = cls.get_all()
        result = []
        for m in models:
            try:
                val = m.__dict__[k]
            except KeyError:
                pass
            else:
                if val == v:
                    result.append(m)
        return result
    
    def __init__(self, d):
        self.id = int(d.get('id', -1))
        self.created_time = int(d.get('created_time', 0))
        self.updated_time = int(d.get('updated_time', 0))
    
    def add(self):
        self.created_time = int(time.time())
        self.updated_time = self.created_time
        self.save()

    def update(self, d):
        self.__dict__.update(d)
        self.updated_time = int(time.time())
        self.save()

    def remove(self):
        if self.id >= 0:
            models = self.get_all()
            index = -1
            for i, m in enumerate(models):
                if self.id == m.id:
                    index = i
                    break
            models.pop(index)
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    def save(self):
        models = self.get_all()
        if self.id == -1:
            if len(models) == 0:
                self.id = 0
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if self.id == m.id:
                    index = i
                    break
            if index != -1:
                models[index] = self
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)
    
    def formatted_ct(self, fmt):
        return formatted_time(self.created_time, fmt)

    def formatted_ut(self, fmt):
        return formatted_time(self.updated_time, fmt)