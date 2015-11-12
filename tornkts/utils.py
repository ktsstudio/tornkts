import errno
from datetime import datetime

import os
from passlib.apps import django10_context as pwd_context

try:
    import ujson as json
except:
    import json as json


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def to_int(value, default=0):
    if type(value) == list:
        if len(value) > 0:
            value = value[0]
        else:
            return default
    try:
        value = int(value)
    except:
        value = default
    return value


def json_dumps(data):
    return json.dumps(data)


def json_loads(data):
    if isinstance(data, str):
        return json.loads(data)
    else:
        return None


def now_date():
    return datetime(datetime.now().year, datetime.now().month, datetime.now().day)


def unique_list(target):
    seen = set()
    return [x for x in target if not (x in seen or seen.add(x))]


class PasswordHelper(object):
    @staticmethod
    def get_hash(text):
        return pwd_context.encrypt(text)

    @staticmethod
    def verify_hash(text, hashed_text):
        try:
            return pwd_context.verify(text, hashed_text)
        except:
            return False


class FileHelper(object):
    @staticmethod
    def file_ext(filename):
        split = filename.rsplit('.', 1)
        if len(split) > 1:
            extension = str(split[1])
            return extension.lower()
        return ""


class InvalidArgumentException(Exception):
    message = ''

    def __init__(self, message):
        super().__init__()
        self.message = message
