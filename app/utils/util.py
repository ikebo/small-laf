import hashlib
from app import app
from app.models.user import User


def _generate_crypt(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def admin_auth(data):
    username = _generate_crypt(data.get('username', None))
    password = _generate_crypt(data.get('password', None))
    print(username, password)
    if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PWD']:
        return True
    return False
