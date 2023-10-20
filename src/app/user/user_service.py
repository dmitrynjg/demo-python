from .entity.user import User


class UserService:
    def info(self, id):
    
      user =  User.query.with_entities(User.id, User.login).filter_by(id=id).first()
    
      return {"id": user[0], "login": user[1]}
