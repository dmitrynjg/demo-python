from flask import Blueprint, g
from src.app.user.user_service import UserService
from src.lib.auth import is_auth
from src.lib.vars.global_prefix import global_prefix

user_service = UserService()
user = Blueprint('user', __name__, url_prefix=f"{global_prefix}/user")


@user.route("/info", methods=['GET'])
@is_auth()
def info():
    return user_service.info(g.user['id'])
