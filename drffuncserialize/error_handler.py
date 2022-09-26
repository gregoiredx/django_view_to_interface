import functools

from django.core.exceptions import ObjectDoesNotExist



class EntityNotFound(Exception):
    pass



def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            raise EntityNotFound

    return wrapper
