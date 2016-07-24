from datetime import datetime

from mongoengine import DateTimeField, EmailField, StringField

from tornkts.base.mongodb import BaseDocument
from tornkts.base.server_response import ServerError


class User(BaseDocument):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    creation_date = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        return super(User, self).save(*args, **kwargs)


class BaseAdmin(User):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }
    email = EmailField(max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    name = StringField(max_length=255, required=False)

    @staticmethod
    def check_repeat(admin, email):
        if admin is None or (admin.email != email):
            email_busy = BaseAdmin.objects(email=email).count()
            if email_busy > 0:
                raise ServerError(ServerError.INVALID_PARAMETER, field='email', field_problem=ServerError.FIELD_REPEAT)

    @property
    def role(self):
        raise NotImplementedError

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'name': self.name,
            'email': self.email,
            'creation_date': self.creation_date,
            'role': self.role
        }
