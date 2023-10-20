from flask import Blueprint, request, jsonify, g
from src.lib.validator import validate_schema, ValidateException
from .schemas.auth_schema import auth_schema
from src.lib.auth import is_auth, encode
from .auth_service import AuthService
from src.lib.vars.global_prefix import global_prefix

auth = Blueprint("auth", __name__, url_prefix=f"{global_prefix}/auth")
authService = AuthService()

@auth.route("/register", methods=["POST"])
@validate_schema(auth_schema)
def register():
    req_data = request.json
    if req_data["password"] == req_data["passwordConfirm"]:
        user = authService.signup(req_data['login'], req_data['password'])
        encoded_jwt = encode(user)

        return jsonify({"message": "Регистрация прошла успешно", "jwt": encoded_jwt})
    raise ValidateException("Пароли не совпадают")


@auth.route("/login", methods=["POST"])
@validate_schema(auth_schema)
def login():
    req_data = request.json
    user = authService.signin(req_data['login'], req_data['password'])
    encoded_jwt = encode(user)
    return jsonify({"message": "Авторизация прошла успешно", "jwt": encoded_jwt})


@auth.route("/test", methods=["GET"])
@is_auth()
def test():
    return g.user
