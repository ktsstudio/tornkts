from tornkts.handlers import BaseHandler
from tornkts.base.server_response import ServerError


class DefaultHandler(BaseHandler):
    def prepare(self):
        super(BaseHandler, self).prepare()
        raise ServerError('not_found')
