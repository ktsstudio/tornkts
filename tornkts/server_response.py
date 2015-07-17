class ServerResponseStatus(object):
    def __init__(self, code, alias, description, http_code=200):
        self.code = code
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

    def get_code(self):
        return self.status.code

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
    ServerResponseStatus(0, 'ok', 'OK', 200),

    ServerResponseStatus(10, 'auth_yet', 'Auth yet', 200),
    ServerResponseStatus(13, 'not_auth', 'Not auth', 403),
    ServerResponseStatus(14, 'role_forbidden', 'For your role access deny', 403),
    ServerResponseStatus(16, 'too_many_requests', 'Too many requests', 403),
    ServerResponseStatus(403, 'account_not_active', 'Account not active', 403),

    ServerResponseStatus(400, 'bad_request', 'Bad request', 400),
    ServerResponseStatus(400, 'invalid_param', 'Invalid param', 400),
    ServerResponseStatus(403, 'forbidden', 'Forbidden', 403),
    ServerResponseStatus(404, 'not_found', 'Not found', 404),
    ServerResponseStatus(405, 'not_implemented', 'Not implemented', 405),
]

UNKNOWN_STATUS = ServerResponseStatus(500, 'unknown_error', 'Unknown error', 500)


def get_response_status_by_code(code):
    for status in STATUSES:
        if code == status.code:
            return status
    return UNKNOWN_STATUS


def get_response_status(alias):
    for status in STATUSES:
        if alias == status.alias:
            return status
    return UNKNOWN_STATUS
