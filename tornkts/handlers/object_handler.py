# coding=utf-8
from tornkts.base.mongodb import get_object_or_none
from tornkts.base.server_response import ServerError
from tornkts.handlers import BaseHandler


class ObjectHandler(BaseHandler):

    MODEL_CLS = None

    @property
    def queryset(self):
        """
        QuerySet, который выполняется в методе get объекта.
        На него навешиваются skip и limit
        """
        return self.MODEL_CLS.objects().all()

    @property
    def put_fields(self):
        """
        Поля, которые принимаются из запроса для добавления/редактирования сущности
        Формат:
        {
            field_name_1: {field_type: int, **kwargs},
            field_name_2: {field_type: str, **kwargs},
            ...
        }
        """
        raise NotImplementedError

    @property
    def get_methods(self):
        return {
            'get': self.get_object
        }

    @property
    def post_methods(self):
        return {
            'save': self.save,
            'delete': self.delete
        }

    def __method_by_field_type(self, field_type):
        return {
            "str": self.get_str_argument,
            "int": self.get_int_argument,
            "bool": self.get_bool_argument,
            "date": self.get_date_argument,
            "email": self.get_email_argument,
            "float": self.get_float_argument,
            "int_array": self.get_int_array_argument,
            "json": self.get_json_argument,
            "mongo_id": self.get_mongo_id_argument,
            "str_array": self.get_str_array_argument,
        }.get(field_type, self.get_argument)

    def get_object(self):
        id = self.get_str_argument('id', default=None)
        if id is None:
            limit = self.get_int_argument('limit', default=20)
            offset = self.get_int_argument('offset', default=0)
            objects = self.queryset.skip(offset).limit(limit)
            objects = [object.to_dict() for object in objects]
            count = self.MODEL_CLS.objects.count()
            response = {
                "items": objects,
                "count": count
            }

            self.send_success_response(data=response)
        else:
            single_object = get_object_or_none(self.MODEL_CLS, id=id)
            if single_object is None:
                raise ServerError('bad_request', data='no_object_{0}'.format(self.MODEL_CLS))
            self.send_success_response(data=single_object.to_dict())

    def save_logic(self, some_object):
        """
        Перед сохранением в методе save вызывается этот метод
        :param some_object: сохраненный объект
        """
        some_object.save()
        self.send_success_response(data=some_object.to_dict())

    def save(self):
        id = self.get_str_argument("id", default=None)
        if id:
            updated_object = get_object_or_none(self.MODEL_CLS)
            return self.put(updated_object=updated_object)
        return self.put()

    def put(self, updated_object=None):
        if updated_object is None:
            updated_object = self.MODEL_CLS()

        for field in self.put_fields:
            kwargs = self.put_fields[field]
            field_type = kwargs.get('field_type', None)
            field_name = kwargs.get('field_name', field)
            argument_method = self.__method_by_field_type(field_type)
            field_data = argument_method(field_name, **kwargs)

            setattr(updated_object, field, field_data)

        self.save_logic(updated_object)

    def delete_logic(self, some_object):
        """
        Определяет логику удаления в методе delete
        :param some_object: удаляемый объект
        :return:
        """
        some_object.delete()
        self.send_success_response()

    def delete(self):
        id = self.get_str_argument("id")
        single_object = get_object_or_none(self.MODEL_CLS, id=id)
        if single_object is None:
            raise ServerError('bad_request', data='no_object_{0}'.format(self.MODEL_CLS))
        self.delete_logic(single_object)
