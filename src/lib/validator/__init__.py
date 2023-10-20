from jsonschema import validate, ValidationError
from functools import wraps
from flask import request
from src.lib.ServerException import ServerException

class ValidateException(ServerException):
    code = 403


def validate_schema(schema):  # Декоратор для валидации по схеме для Flask сервера
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, schema)
            except ValidationError as e:
                raise ValidateException(
                    e.schema.get("message", e.message)[e.validator]
                )  # Здесь мы получаем объект с ошибками и достаем нужное сообщение
            return f(*args, **kw)

        return wrapper

    return decorator
