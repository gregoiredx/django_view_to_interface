from http.client import NOT_FOUND, BAD_REQUEST

from django.http import HttpRequest


def call_view(view, method="GET", query_params=None):
    view_response = view(InternalRequest(method=method, query_params=query_params))
    view_response_data = view_response.data
    if view_response.status_code == NOT_FOUND:
        raise NotFound(data=view_response_data)
    if view_response.status_code == BAD_REQUEST:
        raise InvalidParam(data=view_response_data)
    return view_response_data


class AlwaysAuthorizedUser:
    def is_authenticated(self):
        return True

    def has_perm(self, *args, **kwargs):
        return True


class InternalRequest(HttpRequest):
    _USER = AlwaysAuthorizedUser()

    def __init__(self, method, query_params=None):
        super().__init__()
        self.method = method
        self.GET.update(query_params)
        self._user = self._USER


class NotFound(Exception):
    def __init__(self, data):
        self.data = data


class InvalidParam(Exception):
    def __init__(self, data):
        self.data = data
