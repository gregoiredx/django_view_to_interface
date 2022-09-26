from typing import TypedDict

from drffuncserialize.api import hello_view
from drffuncserialize.view_to_interface import call_view


class CustomerEntity(TypedDict):
    first_name: str
    last_name: str


def hello_interface(pk: int) -> CustomerEntity:
    return call_view(hello_view, query_params={"id": pk})
