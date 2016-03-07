from tornkts.base.server_response import ServerError
from tornkts.handlers.base_handler import BaseHandler


class DefaultHandler(BaseHandler):
    def prepare(self):
        super(BaseHandler, self).prepare()
        raise ServerError(ServerError.NOT_FOUND)
