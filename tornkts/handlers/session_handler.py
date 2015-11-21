import torndsession.session
from tornado.web import RequestHandler
from torndsession.filesession import FileSession


class SessionManager(torndsession.session.SessionManager):
    DEFAULT_SESSION_LIFETIME = 60 * 60 * 24 * 365

    def __init__(self, handler):
        super(SessionManager, self).__init__(handler)

    def destroy(self):
        if isinstance(self.driver, FileSession):
            self.driver.clear(self.handler.get_cookie(self.SESSION_ID))
        else:
            self.driver.client.delete(self.id)
        self._is_dirty = False


class SessionMixin(torndsession.session.SessionMixin):
    @property
    def session(self):
        return self._create_mixin(self, '__session_manager', SessionManager)


class SessionHandler(RequestHandler, SessionMixin):
    was_change = False

    def __init__(self, application, request, **kwargs):
        super(SessionHandler, self).__init__(application, request, **kwargs)

    def data_received(self, chunk):
        pass

    def on_finish(self):
        if self.was_change:
            self.session.flush()  # try to save session

    def session_destroy(self):
        self.session.destroy()

    def session_get(self, key, default=None):
        return self.session.get(key, default)

    def session_set(self, key, value):
        self.was_change = True
        self.session[key] = value

    def session_delete(self, key):
        self.was_change = True
        self.session.delete(key)
