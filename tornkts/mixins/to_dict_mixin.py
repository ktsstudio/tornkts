from tornkts.base.server_response import ServerError


class ToDictMixin(object):
    MODE_INCLUDE = 1
    MODE_EXCLUDE = 0

    def to_dict(self, name='', *args, **kwargs):
        depth = kwargs.get('depth', 0)
        kwargs.update({'depth': depth + 1})

        if depth == 0:
            fields = kwargs.get('fields', None)
        else:
            fields = kwargs.get(name + '_fields', None)

        next_fields = {}
        if isinstance(fields, dict):
            for k, mode in fields.items():
                field = k.split('.', 1)
                if len(field) > 1:
                    entity_title = field[0]
                    fields_chain = field[1]
                    kwargs_key = entity_title + '_fields'

                    if mode == ToDictMixin.MODE_INCLUDE:
                        fields[field[0]] = mode
                    if next_fields.get(kwargs_key) is None:
                        next_fields[kwargs_key] = {}
                    next_fields[kwargs_key][fields_chain] = mode

        kwargs.update(next_fields)
        dict_object = self.to_dict_impl(**kwargs)

        if isinstance(fields, dict):
            mode = None
            for v in fields.values():
                if v != mode and mode is not None:
                    raise ServerError(ServerError.MIX_FIELDS_FILTER)
                mode = v % 2  # MODE_EXCLUDE or MODE_INCLUDE

            for field in dict_object.keys():
                if mode == ToDictMixin.MODE_INCLUDE:
                    if field not in fields.keys():
                        dict_object.pop(field, False)
                elif mode == ToDictMixin.MODE_EXCLUDE:
                    if field in fields.keys():
                        dict_object.pop(field, False)

        return dict_object

    def to_dict_impl(self, **kwargs):
        return {}
