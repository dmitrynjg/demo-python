from flask import Flask, jsonify
from config import Config
from src.app.user.user_controller import user
from src.app.auth.auth_controller import auth
from src.app.product.product_controller import product
from werkzeug.exceptions import HTTPException
from src.lib.validator import ValidateException
from .core.database import db
from src.lib.ServerException import ServerException
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Кастомный обработчик ошибок чтобы ответ был в виде JSON для REST API
@app.errorhandler(Exception)
def handle_exception(error):
    code = 500
    message = 'Произошла ошибка на сервере'
    
    if isinstance(error, HTTPException) or isinstance(error, ValidateException) or isinstance(error, ServerException):
        code = error.code
        message = str(error)

    return jsonify(errorCode=code, error=str(error)), code
    
app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(product)

with app.app_context():
    db.create_all()