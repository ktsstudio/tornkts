# coding=utf-8
import sys

import tornkts.utils as utils
from tornado import httputil
from tornado.log import gen_log
from tornado.web import HTTPError, Finish, app_log, MissingArgumentError
from tornkts.base.server_response import ServerResponseStatus, ServerError
from tornkts.mixins.arguments_mixin import ArgumentsMixin
from .session_handler import SessionHandler


class BaseHandler(SessionHandler, ArgumentsMixin):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_argument(self, name, default=SessionHandler._ARG_DEFAULT, strip=True):
        try:
            value = super(BaseHandler, self).get_argument(name, default, strip)
        except MissingArgumentError:
            raise ServerError(ServerError.BAD_REQUEST, field=name, field_problem=ServerError.FIELD_SKIPPED)
        return value

    def data_received(self, chunk):
        pass

    @property
    def client_version(self):
        return self.get_float_argument('v', default=1)

    @property
    def default_get_method(self):
        return None

    @property
    def default_post_method(self):
        return None

    @property
    def get_methods(self):
        return {}

    @property
    def post_methods(self):
        return {}

    def get(self, *args, **kwargs):
        action_title = args[0] if len(args) > 0 else ''

        if not (action_title in self.get_methods.keys()):
            action_title = self.default_get_method
        if action_title in self.get_methods.keys():
            return self.get_methods.get(action_title)()

        if action_title in self.post_methods:
            raise ServerError(ServerError.NOT_IMPLEMENTED)
        else:
            raise ServerError(ServerError.NOT_FOUND)

    def post(self, *args, **kwargs):
        action_title = args[0] if len(args) > 0 else ''

        if not (action_title in self.post_methods.keys()):
            action_title = self.default_post_method
        if action_title in self.post_methods.keys():
            return self.post_methods.get(action_title)()

        if action_title in self.get_methods:
            raise ServerError(ServerError.NOT_IMPLEMENTED)
        else:
            raise ServerError(ServerError.NOT_FOUND)

    def head(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def delete(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def patch(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def put(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    def options(self, *args, **kwargs):
        raise ServerError(ServerError.NOT_IMPLEMENTED)

    @property
    def current_user_id(self):
        if self.current_user is not None:
            return self.current_user.get_id()
        else:
            return None

    @property
    def current_user_role(self):
        if self.current_user is not None:
            return self.current_user.role
        else:
            return None

    def _handle_request_exception(self, e):
        if isinstance(e, Finish):
            if not self._finished:
                self.finish()
            return
        self.log_exception(*sys.exc_info())
        if self._finished:
            return
        if isinstance(e, HTTPError):
            if e.status_code not in httputil.responses and not e.reason:
                gen_log.error("Bad HTTP status code: %d", e.status_code)
                self.send_error(ServerError.INTERNAL_SERVER_ERROR, exc_info=sys.exc_info())
            else:
                self.send_error(ServerResponseStatus('http_error', e.reason, e.status_code), exc_info=sys.exc_info())
        elif isinstance(e, ServerError):
            self.send_error(e.status, exc_info=sys.exc_info())
        else:
            self.send_error(exc_info=sys.exc_info())

    def send_error(self, status=ServerError.INTERNAL_SERVER_ERROR, **kwargs):
        if not isinstance(status, ServerResponseStatus):
            status = ServerError.UNKNOWN

        if self._headers_written:
            gen_log.error("Cannot send error response after headers written")
            if not self._finished:
                self.finish()
            return
        self.clear()

        reason = None
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, HTTPError) and exception.reason:
                reason = exception.reason

        self.set_status(status_code=status.http_code, reason=reason)
        try:
            self.write_error(status, **kwargs)
        except Exception:
            app_log.error("Uncaught exception in write_error", exc_info=True)
        if not self._finished:
            self.finish()

    def write_error(self, status=ServerError.INTERNAL_SERVER_ERROR, **kwargs):
        if not isinstance(status, ServerResponseStatus):
            status = ServerError.UNKNOWN

        exception = kwargs['exc_info'][1]
        data = None
        field = None
        field_problem = None

        if isinstance(exception, HTTPError) and exception.log_message is not None:
            message = exception.log_message
        elif isinstance(exception, ServerError):
            message = exception.get_description()
            data = exception.get_data()
            field = exception.get_field()
            field_problem = exception.get_field_problem()
        else:
            message = self._reason
        self.send_response(status=status, message=message, data=data, field=field, field_problem=field_problem)

    def set_content_type_json(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def set_content_type_plain(self):
        self.set_header("Content-Type", "text/plain; charset=UTF-8")

    def send_success_response(self, message=None, data=None):
        self.send_response(status=ServerError.OK, message=message, data=data)

    def send_response(self, status=ServerError.OK, message=None, data=None, field=None, field_problem=None):
        if not isinstance(status, ServerResponseStatus):
            status = ServerError.UNKNOWN

        if data is None:
            data = {}

        self.set_status(status.http_code)

        response = {
            'status': status.alias,
            'data': data
        }

        if message is not None:
            response['message'] = message

        if field is not None:
            response['field'] = field
        if field_problem is not None:
            response['field_problem'] = field_problem

        self.write(utils.json_dumps(response))

    def log_exception(self, typ, value, tb):
        if not isinstance(value, ServerError):
            super(BaseHandler, self).log_exception(typ, value, tb)

    def write_raw(self, chunk):
        self.write(chunk, plain=True)

    def write(self, chunk, plain=False, nocontenttype=False):
        if not nocontenttype:
            if plain:
                self.set_content_type_plain()
            else:
                self.set_content_type_json()
        self.set_header('Cache-control', 'no-cache,no-store,must-revalidate')
        super(BaseHandler, self).write(chunk)
