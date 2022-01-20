import hashlib
from myapp import app
from myapp.models import *





def add_user(name,username,pasword, **kwargs):
    pasword = str(hashlib.md5(pasword.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                pasword=pasword,
                email = kwargs.get('email'),
                sdt=kwargs.get('sdt'),
                avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

def check_login(username,pasword):
    if username and pasword:
        pasword = str(hashlib.md5(pasword.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.pasword.__eq__(pasword)).first()


def check_adminlogin(username,pasword):
    if username and pasword:
        pasword = str(hashlib.md5(pasword.strip().encode('utf-8')).hexdigest())
        admin = User.query.filter(User.user_role.__eq__("ADMIN"))
        return admin.filter(User.username.__eq__(username.strip()),
                                 User.pasword.__eq__(pasword)).first()
def get_user_by_id(user_id):
    return User.query.get(user_id)