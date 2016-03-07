# coding=utf-8
from tornkts.base.mongodb import get_object_or_none
from tornkts.base.server_response import ServerError, ServerResponseStatus
from tornkts.handlers import BaseHandler
from tornkts.modules.verification import Verification


class VerificationHandler(BaseHandler):
    STATUS_SMS_SEND_FAIL = ServerResponseStatus('sms_send_fail', 'fail to send some sms', 406),
    STATUS_VERIFICATION_NOT_FOUND = ServerResponseStatus('verification_not_found', 'no requested verification', 400),
    STATUS_INVALID_VERIFICATION_KEY = ServerResponseStatus('invalid_verification_key', 'incorrect verification key',
                                                           403),
    STATUS_NOT_VERIFIED = ServerResponseStatus('not_verified', 'not verified yet', 403),

    def keygen(self):
        import random
        return unicode(random.randint(10000, 100000))

    def send(self, verification):
        """
        Метод отправки пользователю ключа
        Нужно вернуть true/false. Удалось ли отправить код
        """
        raise NotImplementedError

    def get_verified_argument(self):
        """
        Получение телефона/email'а и тд
        :return:
        """
        return self.get_str_argument("phone")

    @property
    def post_methods(self):
        return {
            'verify': self._verify
        }

    @property
    def get_methods(self):
        return {
            'get_key': self.get_verification_key,
        }

    def get_verification_key(self):
        verified_entity = self.get_verified_argument()

        verification = get_object_or_none(Verification, verified_entity=verified_entity)

        if verification is None:
            verification = Verification.generate(verified_entity, self.keygen)

        if self.send(verification):
            verification.save()

        self.send_success_response()

    @staticmethod
    def verify(verified_entity, verification_key):
        """
        Метод должен райзить ошибки
        :param verified_entity: сущность
        :param verification_key: ключ
        :return:
        """
        verification = get_object_or_none(Verification, verified_entity=verified_entity)

        if verification is None:
            raise ServerError(VerificationHandler.STATUS_VERIFICATION_NOT_FOUND)
        if not verification.verify(verification_key):
            raise ServerError(VerificationHandler.STATUS_INVALID_VERIFICATION_KEY)

        verification.verified = True
        verification.save()

    def _verify(self):
        verified_entity = self.get_verified_argument()
        verification_key = self.get_str_argument("verification_key")

        self.verify(verified_entity, verification_key)

        self.send_success_response()
