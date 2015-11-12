from mongoengine import Document
from tornkts.mixins.to_dict_mixin import ToDictMixin


class BaseDocument(ToDictMixin, Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    def get_id(self):
        return str(self.pk)

