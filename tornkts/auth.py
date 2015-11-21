import functools
from tornado import gen
from tornkts.base.server_response import ServerError


def need_role(role=None, async=False):
    if not role:
        role = []

    def generator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                raise ServerError('not_auth')
            elif self.current_user.role not in role:
                raise ServerError('role_forbidden')
            return method(self, *args, **kwargs)

        @functools.wraps(method)
        @gen.coroutine
        def async_wrapper(self, *args, **kwargs):
            current_user = yield self.current_user
            if not current_user:
                raise ServerError('not_auth')
            elif current_user.role not in role:
                raise ServerError('role_forbidden')
            yield method(self, *args, **kwargs)

        if async:
            return async_wrapper
        else:
            return wrapper

    return generator


def need_not_role(role=None, error_code='ok', async=False):
    if not role:
        role = []

    def generator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user and self.current_user.role in role:
                raise ServerError(error_code)
            return method(self, *args, **kwargs)

        @functools.wraps(method)
        @gen.coroutine
        def async_wrapper(self, *args, **kwargs):
            current_user = yield self.current_user
            if current_user and current_user.role in role:
                raise ServerError(error_code)
            yield method(self, *args, **kwargs)

        if async:
            return async_wrapper
        else:
            return wrapper

    return generator


def need_is_approved(role=None):
    if not role:
        role = []

    def generator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                raise ServerError('not_auth')
            elif self.current_user.role in role and self.current_user.is_approved is not True:
                raise ServerError('forbidden')
            return method(self, *args, **kwargs)

        return wrapper

    return generator


def need_is_active(role=None):
    if not role:
        role = []

    def generator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user and self.current_user.role in role:
                if self.current_user.is_active is not True:
                    raise ServerError('account_not_active')
            return method(self, *args, **kwargs)

        return wrapper

    return generator


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise ServerError('not_auth')
        return method(self, *args, **kwargs)

    return wrapper


def not_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            raise ServerError('auth_yet')
        return method(self, *args, **kwargs)

    return wrapper
