from datetime import datetime
from mongoengine import DateTimeField, EmailField, StringField
from tornkts.base.mongodb import BaseDocument


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