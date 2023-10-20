from functools import wraps
from flask import request, g
from src.lib.ServerException import ServerException
import jwt
from datetime import datetime, timezone
from src.app.user.entity.user import User

secret_jwt = "SecretSalt"


class AuthException(ServerException):
    code = 401


def encode(data):
    timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    data["iat"] = timestamp
    return jwt.encode(
        data,
        secret_jwt,
        algorithm="HS256",
    )


def decode(jwt_code):
    return jwt.decode(
        jwt_code,
        secret_jwt,
        algorithms=["HS256"],
    )


def is_auth():  # Декоратор для проверки авторизации пользователя
    def decorator(f):
        @wraps(f)
        def wrapper():
            if not request.headers.get("Authorization"):
                raise AuthException("Вы не авторизованы")
            jwt_split_bearer = request.headers["Authorization"].split("Bearer ")
            if len(jwt_split_bearer) == 1:
                raise AuthException("Неправильно передан jwt")
            jwt_header = jwt_split_bearer[1]

            data = decode(jwt_header)

            find_user = User.query.filter_by(id=data['id']).with_entities(User.id).first()
            

            if find_user is not None:
                g.user = { "id": find_user[0] }
                return f()
            raise AuthException("Вы не авторизованы")

        return wrapper

    return decorator
