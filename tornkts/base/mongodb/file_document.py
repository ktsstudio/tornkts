from mongoengine import StringField
from tornkts.base.mongodb.base_document import BaseDocument


class FileDocument(BaseDocument):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    file_id = StringField()
    file_url = StringField()

    def to_dict_impl(self, **kwargs):
        return {
            "file_id": self.file_id,
            "file_url": self.file_url,
            "id": self.get_id()
        }
