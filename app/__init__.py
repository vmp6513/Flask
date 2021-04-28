from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

from config import config  # a dict variable

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()

login_manager = LoginManager()
# 设置登录页面的端点（路由），记住要加上蓝本名
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    # 从对象中读取配置
    app.config.from_object(config[config_name])
    # staticmethod
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
    