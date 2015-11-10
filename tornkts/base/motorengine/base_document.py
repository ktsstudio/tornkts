from motorengine import document
from tornkts.mixins.to_dict_mixin import ToDictMixin
from tornkts.mixins.validate_mixin import ValidateMixin

class BaseDocument(ToDictMixin, ValidateMixin, document.Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    def get_id(self):
        return str(self._id)
