class ServerResponseStatus(object):
    def __init__(self, status_alias, status_description, http_code=200):
        self.alias = status_alias
        self.description = status_description
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

    # --- Error Statuses ---
    OK = ServerResponseStatus('ok', 'OK', 200)

    BAD_REQUEST = ServerResponseStatus('bad_request', 'Bad request', 400)
    INVALID_PARAMETER = ServerResponseStatus('invalid_param', 'Invalid parameter', 400)
    AUTH_NOT_REQUIRED = ServerResponseStatus('auth_not_required', 'Authentication not required', 400)

    AUTH_REQUIRED = ServerResponseStatus('auth_required', 'Authentication required', 401)
    ACCESS_DENIED = ServerResponseStatus('access_denied', 'Access denied', 401)

    FORBIDDEN = ServerResponseStatus('forbidden', 'Forbidden', 403)
    INVALID_CREDENTIALS = ServerResponseStatus('invalid_credentials', 'Invalid credentials', 403)
    ROLE_FORBIDDEN = ServerResponseStatus('role_forbidden', 'For your role access denied', 403)
    ACCOUNT_INACTIVE = ServerResponseStatus('account_not_active', 'Account is not active', 403)

    NOT_FOUND = ServerResponseStatus('not_found', 'Not found', 404)

    NOT_IMPLEMENTED = ServerResponseStatus('not_implemented', 'Not implemented', 405)

    TOO_MANY_REQUESTS = ServerResponseStatus('too_many_requests', 'Too many requests', 429)

    MIX_FIELDS_FILTER = ServerResponseStatus('mix_fields_filter', 'Cannot have a mix of inclusion and exclusion', 500)
    STORAGE_ERROR = ServerResponseStatus('storage_error', 'Storage error', 500)
    INTERNAL_SERVER_ERROR = ServerResponseStatus('internal_error', 'Internal server error', 500)
    UNKNOWN = ServerResponseStatus('unknown_error', 'Unknown error', 500)
    FILE_SAVE_ERROR = ServerResponseStatus('file_save_error', "Can't save data", 500)

    # ------------------------

    def __init__(self, status, description=None, data=None, field=None, field_problem=None):
        if not isinstance(status, ServerResponseStatus):
            status = self.UNKNOWN

        self.status = status
        self.description = self.status.description
        if isinstance(description, str):
            self.description = description

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
