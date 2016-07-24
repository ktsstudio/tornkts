from mongoengine import ValidationError

from tornkts.base.server_response import ServerError


class ValidateMixin(object):
    def validate_model(self, prefix=None):
        if prefix is not None:
            prefix += '.'
        else:
            prefix = ''
        try:
            self.validate()
        except ValidationError as e:
            field = e.errors.keys().pop()
            raise ServerError(ServerError.INVALID_PARAMETER,
                              field=prefix + str(field),
                              field_problem=ServerError.FIELD_INVALID_FORMAT)