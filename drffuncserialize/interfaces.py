from typing import TypedDict

from drffuncserialize.api import get_customer_view
from drffuncserialize.view_to_interface import call_view


class CustomerEntity(TypedDict):
    first_name: str
    last_name: str


def get_customer(pk: int) -> CustomerEntity:
    return call_view(get_customer_view, query_params={"id": pk})
