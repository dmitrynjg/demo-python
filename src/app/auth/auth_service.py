from src.core.database import db
from ..user.entity.user import User
from src.lib.ServerException import ServerException
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def signup(self, username: str, password: str):
        findUser = User.query.filter_by(login=username).first()
        if findUser is not None:
            raise ServerException("Такой пользователь уже существует")
        hashed_password = generate_password_hash(password, salt_length=10)
        user = User(login=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {"id": user.id}

    def signin(self, login: str, password: str):
        find_user = User.query.filter_by(login=login).first()
        if find_user is None or not check_password_hash(find_user.password, password):
            raise ServerException("Логин или пароль неверный")
         
        return {"id": find_user.to_dict()['id']}