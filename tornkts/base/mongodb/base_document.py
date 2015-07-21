from mongoengine import document


class BaseDocument(document.Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    def get_id(self):
        return str(self.pk)

    def to_dict(self, *args, **kwargs):
        dict_object = self.to_dict_impl(**kwargs)
        mode = kwargs.get('mode', 'include')

        if mode == 'include':
            for key in kwargs.keys():
                if not kwargs.get(key):
                    dict_object.pop(key, False)
        elif mode == 'list':
            for dict_object_key in dict_object.keys():
                if kwargs.get(dict_object_key, True):
                    dict_object.pop(dict_object_key, False)

        return dict_object

    def to_dict_impl(self, **kwargs):
        return {}
