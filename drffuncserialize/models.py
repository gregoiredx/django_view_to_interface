from django.db.models import Model, CharField


class Customer(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
