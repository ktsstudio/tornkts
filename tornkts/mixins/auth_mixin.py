from tornkts.base.mongodb.utils import get_object_or_none
from tornkts.base.server_response import ServerError
from tornkts.utils import PasswordHelper


class AuthMixin(object):
    """
    Mixin for authorization in tornkts handler
    Use email+password
    Find users by email for auth_classes list
    """

    @property
    def auth_classes(self):
        """
        Example: return [Admin, Moderator...]
        :return: List of auth classes
        """
        raise NotImplementedError

    def auth(self):
        email = self.get_argument('email')
        password = self.get_argument('password')

        admin = None
        for auth_cls in self.auth_classes:
            role = [auth_cls.role]
            admin = get_object_or_none(auth_cls, email=email)
            if admin is not None: break

        if admin is None:
            raise ServerError(ServerError.INVALID_CREDENTIALS)

        if self.current_user and self.current_user.role in role:
            raise ServerError(ServerError.AUTH_NOT_REQUIRED)

        if not PasswordHelper.verify_hash(password, admin.password):
            raise ServerError(ServerError.INVALID_CREDENTIALS)

        self.session_set('user_id', admin.get_id())
        self.session_set('is_auth', True)

        self.send_success_response()

    def get_current_user(self):
        if self.session_get('is_auth', False):
            user_id = self.session_get('user_id', '*')

            user = None
            for auth_cls in self.auth_classes:
                user = get_object_or_none(auth_cls, pk=user_id)
                if user is not None: break

            if user is None:
                return False

            return user
        else:
            return False



