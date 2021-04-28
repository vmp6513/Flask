from flask import Blueprint

main = Blueprint('main', __name__)
# 避免循环导入依赖
from . import errors, views

from ..models import Permission

# 使用上下文处理器，将Permission变量在所有模板中能够访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)