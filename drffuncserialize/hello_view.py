from dataclasses import dataclass
from typing import TypedDict

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.util import underscoreize
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.fields import CharField, IntegerField
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from drffuncserialize.error_handler import handle_errors
from drffuncserialize.models import Customer


class QueryParamSerializer(Serializer):
    id = IntegerField(source="pk")


class ResponseSerializer(Serializer):
    first_name = CharField()
    last_name = CharField()


@dataclass
class CustomerEntity:
    first_name: str
    last_name: str


@api_view()
@renderer_classes((CamelCaseJSONRenderer,))
def hello_view(request: Request):
    raw_params = underscoreize(request.query_params)
    response_data = hello_common(raw_params)
    return Response(response_data)


@handle_errors
def hello_interface(pk: int) -> CustomerEntity:
    return CustomerEntity(**hello_common({"id": pk}))


def hello_common(params):
    query_params_serializer = QueryParamSerializer(data=params)
    query_params_serializer.is_valid(raise_exception=True)
    validated_params = query_params_serializer.validated_data
    pk = validated_params["pk"]
    customer = Customer.objects.get(pk=pk)
    response_data = ResponseSerializer(customer).data
    return response_data
