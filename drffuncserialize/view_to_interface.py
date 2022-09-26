from django.http import HttpRequest

from drffuncserialize.errors import EntityNotFound


class FakeRequest(HttpRequest):
    def __init__(self, query_params=None):
        self._query_params = query_params

    @property
    def GET(self):
        return self._query_params

    @property
    def META(self):
        return {}

    @property
    def method(self):
        return "GET"


def call_view(view, query_params=None):
    view_response = view(FakeRequest(query_params=query_params))
    view_response_data = view_response.data
    if view_response.status_code == 404:
        raise EntityNotFound(data=view_response_data)
    return view_response_data
