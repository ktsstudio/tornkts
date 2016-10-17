import errno
import mimetypes
from datetime import datetime
import os

import six
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
    try:
        return json.loads(data)
    except:
        return None


def now_date():
    return datetime(datetime.now().year, datetime.now().month, datetime.now().day)


def unique_list(target):
    seen = set()
    return [x for x in target if not (x in seen or seen.add(x))]


def encode_multipart_formdata(fields=None, files=None):
    if fields is None:
        fields = {}
    if files is None:
        files = {}

    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n' if six.PY2 else b'\r\n'
    L = []

    for (key, value) in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)

    for (key, filename, value) in files:
        if six.PY2:
            filename = filename.encode("utf8")
        L.append('--' + BOUNDARY)
        L.append(
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                key, filename
            )
        )
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)

    L.append('--' + BOUNDARY + '--')
    L.append('')

    if six.PY3:
        for i in range(len(L)):
            if isinstance(L[i], int):
                L[i] = str(L[i])
            if isinstance(L[i], str):
                L[i] = str.encode(L[i])

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


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
