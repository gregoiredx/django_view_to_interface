import pytest

from drffuncserialize.error_handler import EntityNotFound
from drffuncserialize.hello_view import hello_interface
from drffuncserialize.models import Customer


@pytest.fixture
def customer():
    return Customer.objects.create(first_name="John", last_name="Doe")


@pytest.mark.django_db
def test_python_ok(customer):
    customer_entity = hello_interface(pk=customer.pk)
    assert customer_entity.first_name == 'John'
    assert customer_entity.last_name == 'Doe'


@pytest.mark.django_db
def test_http_ok(client, customer):
    assert client.get(f'/hello?id={customer.pk}').json() == {'firstName': 'John', 'lastName': 'Doe'}


@pytest.mark.django_db
def test_python_not_found(customer):
    with pytest.raises(EntityNotFound):
        hello_interface(pk=42)


@pytest.mark.django_db
def test_http_not_found(client, customer):
    assert client.get(f'/hello?id=42').status_code == 404
