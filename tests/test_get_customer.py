import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from drffuncserialize.view_to_interface import NotFound, InvalidParam
from drffuncserialize.interfaces import get_customer
from drffuncserialize.models import Customer


@pytest.fixture
def customer():
    return Customer.objects.create(first_name="John", last_name="Doe")


@pytest.fixture
def authorized_user():
    user = User.objects.create()
    user.user_permissions.add(
        Permission.objects.get(codename='view_customer', content_type=(ContentType.objects.get_for_model(Customer)))
    )
    return user


@pytest.mark.django_db
def test_http_ok(client, authorized_user, customer):
    client.force_login(authorized_user)
    assert client.get(f'/hello?id={customer.pk}').json() == {'firstName': 'John', 'lastName': 'Doe'}


@pytest.mark.django_db
def test_python_ok(customer):
    customer_entity = get_customer(pk=customer.pk)
    assert customer_entity['first_name'] == 'John'
    assert customer_entity['last_name'] == 'Doe'


@pytest.mark.django_db
def test_http_not_found(client, authorized_user, customer):
    client.force_login(authorized_user)
    assert client.get(f'/hello?id=42').status_code == 404


@pytest.mark.django_db
def test_python_not_found(customer):
    with pytest.raises(NotFound):
        get_customer(pk=42)


@pytest.mark.django_db
def test_http_unauthorized(client, customer):
    user = User.objects.create()
    client.force_login(user)
    assert client.get(f'/hello?id=42').status_code == 403


@pytest.mark.django_db
def test_http_invalid_param(client, authorized_user, customer):
    client.force_login(authorized_user)
    assert client.get(f'/hello?id=john').status_code == 400


@pytest.mark.django_db
def test_python_invalid_param(customer):
    with pytest.raises(InvalidParam):
        get_customer(pk="john")
