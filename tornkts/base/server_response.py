class ServerResponseStatus(object):
    def __init__(self, alias, description, http_code=200):
        self.alias = alias
        self.description = description
        self.http_code = http_code


class ServerError(Exception):
    FIELD_INVALID_FORMAT = 'invalid_format'
    FIELD_LESS_MIN = 'less_min'
    FIELD_MORE_MAX = 'more_max'
    FIELD_NOT_EMAIL = 'not_email'
    FIELD_EMPTY = 'empty'
    FIELD_SKIPPED = 'skipped'
    FIELD_NOT_ALLOWED = 'not_allowed'
    FIELD_REPEAT = 'repeat'
    FIELD_INVALID = 'invalid'

    def __init__(self, status_alias, description=None, data=None, field=None, field_problem=None):
        self.status = get_response_status(status_alias)
        if description is not None:
            self.description = description
        else:
            self.description = self.status.description

        self.data = data
        self.field = field
        self.field_problem = field_problem

    def get_http_code(self):
        return self.status.http_code

    def get_description(self):
        return self.description

    def get_alias(self):
        return self.status.alias

    def get_data(self):
        return self.data

    def get_field(self):
        return self.field

    def get_field_problem(self):
        return self.field_problem


STATUSES = [
    ServerResponseStatus('ok', 'OK', 200),

    ServerResponseStatus('auth_yet', 'Auth yet', 200),
    ServerResponseStatus('not_auth', 'Not auth', 403),
    ServerResponseStatus('role_forbidden', 'For your role access deny', 403),
    ServerResponseStatus('too_many_requests', 'Too many requests', 403),
    ServerResponseStatus('account_not_active', 'Account not active', 403),

    ServerResponseStatus('bad_request', 'Bad request', 400),
    ServerResponseStatus('invalid_param', 'Invalid param', 400),
    ServerResponseStatus('forbidden', 'Forbidden', 403),
    ServerResponseStatus('not_found', 'Not found', 404),
    ServerResponseStatus('not_implemented', 'Not implemented', 405),
    
    ServerResponseStatus('mix_fields_filter', 'Cannot have a mix of inclusion and exclusion', 500)
]

UNKNOWN_STATUS = ServerResponseStatus('unknown_error', 'Unknown error', 500)


def get_response_status_by_code(code):
    for status in STATUSES:
        if code == status.http_code:
            return status
    return UNKNOWN_STATUS


def get_response_status(alias):
    for status in STATUSES:
        if alias == status.alias:
            return status
    return UNKNOWN_STATUS
