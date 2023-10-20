from src.core.database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), unique=True)
    __password = db.Column(db.String(128), name='password')  # Задаем имя столбца 'password'

    def to_dict(self):
        return {"id": self.id, "login": self.login, "password": self.__password}

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    password = property(get_password, set_password)