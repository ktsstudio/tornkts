# coding=utf-8
import json
from datetime import datetime

import re
import six
from tornkts.base.server_response import ServerError


class ArgumentsMixin(object):
    EMAIL_REGEX = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,253}[A-Z0-9])?\.)+[A-Z]{2,6}$', re.IGNORECASE  # domain
    )

    MIN_DATE = datetime.strptime('1900-01-01', '%Y-%m-%d')

    STR_TYPE = unicode if six.PY2 else str
    INT_MAX = 18446744073709551616 if six.PY3 else 4294967295

    def _clear_kwargs(self, kwargs):
        return dict((k, v) for k, v in kwargs.items() if k in ['default', 'strip'])

    def get_mongo_id_argument(self, name, **kwargs):
        argument = self.get_str_argument(name, **kwargs)
        if argument != kwargs.get('default'):
            if len(argument) != 24 or len(re.findall('[^A-Ha-h0-9]', argument)) > 0:
                raise ServerError(ServerError.INVALID_PARAMETER, description='Argument %s is not mongo id' % name,
                                  field=name,
                                  field_problem=ServerError.FIELD_INVALID_FORMAT)
        return argument

    def get_int_argument(self, name, **kwargs):
        argument = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if argument != kwargs.get('default'):
                if argument == '' and 'default' in kwargs:
                    argument = kwargs.get('default')
                else:
                    argument = int(argument)
            else:
                return argument
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER, description='Argument %s is not int' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)

        if kwargs.get('min', None) is not None:
            min_value = int(kwargs.get('min'))
            if argument < min_value:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Argument %s must be greater than %s' % (name, min_value),
                                  field=name,
                                  field_problem=ServerError.FIELD_LESS_MIN)
        if kwargs.get('max', None) is not None:
            max_value = int(kwargs.get('max', self.INT_MAX))
            if argument > max_value:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Argument %s must be less than than %s' % (name, max_value),
                                  field=name,
                                  field_problem=ServerError.FIELD_MORE_MAX)
        if kwargs.get('allowed_values', None) is not None:
            allowed_values = kwargs.get('allowed_values', None)
            if argument not in allowed_values:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Value %s is not allowed' % argument,
                                  field=name,
                                  field_problem=ServerError.FIELD_NOT_ALLOWED)
        return argument

    def get_bool_argument(self, name, **kwargs):
        argument = self.get_str_argument(name, **kwargs)
        try:
            if argument != kwargs.get('default'):
                if argument.lower() == 'true':
                    argument = True
                else:
                    argument = False
            else:
                return argument
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER, description='Argument %s is not bool' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)
        return argument

    def get_email_argument(self, name, **kwargs):
        argument = self.get_str_argument(name, **kwargs)
        if argument != kwargs.get('default'):
            if not (argument == '' and kwargs.get('empty', False)):
                if not ArgumentsMixin.EMAIL_REGEX.match(argument):
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Argument %s have bad email format' % name,
                                      field=name,
                                      field_problem=ServerError.FIELD_NOT_EMAIL)
        return argument

    def get_float_argument(self, name, **kwargs):
        argument = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if argument != kwargs.get('default'):
                argument = argument.replace(',', '.')
                argument = float(argument)
            else:
                return argument
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Argument %s is not number' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)

        if kwargs.get('min', None) is not None:
            min_value = float(kwargs.get('min'))
            if argument < min_value:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Argument %s must be greater than %s' % (name, min_value),
                                  field=name,
                                  field_problem=ServerError.FIELD_LESS_MIN)
        if kwargs.get('max', None) is not None:
            max_value = float(kwargs.get('max'))
            if argument > max_value:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Argument %s must be less than than %s' % (name, max_value),
                                  field=name,
                                  field_problem=ServerError.FIELD_MORE_MAX)
        return argument

    def get_int_array_argument(self, name, **kwargs):
        arguments = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if arguments != kwargs.get('default'):
                if arguments == '':
                    return []
                arguments = [int(x) for x in arguments.split(',')]
            else:
                return arguments
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER, description='Argument %s is not int' % name, field=name)

        if kwargs.get('min', None) is not None:
            min_value = int(kwargs.get('min'))
            for argument in arguments:
                if argument < min_value:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Argument %s must be greater than %s' % (name, min_value),
                                      field=name,
                                      field_problem=ServerError.FIELD_LESS_MIN)
        if kwargs.get('max', None) is not None:
            max_value = int(kwargs.get('max', self.INT_MAX))
            for argument in arguments:
                if argument > max_value:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Argument %s must be less than than %s' % (name, max_value),
                                      field=name,
                                      field_problem=ServerError.FIELD_MORE_MAX)
        return arguments

    def get_str_argument(self, name, **kwargs):
        argument = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if argument != kwargs.get('default'):
                argument = self.STR_TYPE(argument)
            else:
                return argument
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Argument %s is cant convert to string' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)

        def check():
            if kwargs.get('length_min', None) is not None:
                length_min = int(kwargs.get('length_min'))
                if len(argument) < length_min:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Length of argument %s must be greater than %s' % (name, length_min),
                                      field=name,
                                      field_problem=ServerError.FIELD_LESS_MIN)
            if kwargs.get('length_max', None) is not None:
                length_max = int(kwargs.get('length_max'))
                if len(argument) > length_max:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Length of argument %s must be less than than %s' % (
                                          name, length_max),
                                      field=name,
                                      field_problem=ServerError.FIELD_MORE_MAX)

            # Аналог length_min == 1
            if kwargs.get('empty', None) is not None:
                empty = bool(kwargs.get('empty', None))
                if len(argument) == 0 and empty is False:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Argument %s cannot be empty' % name,
                                      field=name,
                                      field_problem=ServerError.FIELD_EMPTY)

            if kwargs.get('allowed_values', None) is not None:
                allowed_values = kwargs.get('allowed_values', None)
                if argument not in allowed_values:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Value %s is not allowed' % argument,
                                      field=name,
                                      field_problem=ServerError.FIELD_NOT_ALLOWED)

        if kwargs.get('none_if_empty', False) is True:
            if len(argument) == 0:
                argument = None

        check()

        if kwargs.get('clear_regexp', None) is not None:
            clear_regexp = kwargs.get('clear_regexp')
            argument = re.sub(clear_regexp, '', argument)
        try:
            check()
        except ServerError:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Value %s have invalid format' % argument,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)
        return argument

    def get_str_array_argument(self, name, **kwargs):
        arguments = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if arguments != kwargs.get('default'):
                arguments = [self.STR_TYPE(x) for x in arguments.split(',')]
            else:
                return arguments
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Argument %s is not str' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)

        if kwargs.get('empty', None) is not None:
            empty = bool(kwargs.get('empty', None))
            for argument in arguments:
                if len(argument) == 0 and empty is False:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Argument %s have empty elements' % name,
                                      field=name,
                                      field_problem=ServerError.FIELD_EMPTY)

        if kwargs.get('allowed_values', None) is not None:
            allowed_values = kwargs.get('allowed_values', None)
            for argument in arguments:
                if argument not in allowed_values:
                    raise ServerError(ServerError.INVALID_PARAMETER,
                                      description='Value %s is not allowed' % argument,
                                      field=name,
                                      field_problem=ServerError.FIELD_NOT_ALLOWED)

        return arguments

    def get_date_argument(self, name, date_format, **kwargs):
        argument = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if argument != kwargs.get('default'):
                argument = datetime.strptime(argument, date_format)
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Argument %s have invalid format. Valid format: %s' % (name, date_format),
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)
        if kwargs.get('min', ArgumentsMixin.MIN_DATE) is not None and not kwargs.get('ignore_min', False):
            min_value = kwargs.get('min', ArgumentsMixin.MIN_DATE)
            if isinstance(min_value, datetime) and argument < min_value:
                raise ServerError(ServerError.INVALID_PARAMETER,
                                  description='Argument %s must be greater than %s' % (
                                      name, min_value.strftime('%Y-%m-%d %H:%M:%S')),
                                  field=name,
                                  field_problem=ServerError.FIELD_LESS_MIN)
        return argument

    def get_json_argument(self, name, **kwargs):
        argument = self.get_argument(name, **self._clear_kwargs(kwargs))
        try:
            if argument != kwargs.get('default'):
                argument = json.loads(argument)
        except Exception:
            raise ServerError(ServerError.INVALID_PARAMETER,
                              description='Argument %s is invalid json' % name,
                              field=name,
                              field_problem=ServerError.FIELD_INVALID_FORMAT)
        return argument
