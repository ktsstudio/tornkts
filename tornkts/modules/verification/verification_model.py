# coding=utf-8
from mongoengine import StringField, BooleanField
from tornkts.base.mongodb import BaseDocument


class Verification(BaseDocument):
    verified_entity = StringField(unique=True)
    key = StringField()
    verified = BooleanField(default=False)

    @classmethod
    def generate(self, verified, keygen):
        """
        :param verified: телефон или email (verified_entity)
        :param keygen: функция генерации ключа
        :return:
        """
        return Verification(
            verified_entity=verified,
            key=keygen(),
            verified=False
        )

    def verify(self, key):
        return self.key == key