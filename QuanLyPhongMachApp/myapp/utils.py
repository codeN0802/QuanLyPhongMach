import hashlib
from myapp import app
from myapp.models import *
from flask_login import current_user
from sqlalchemy.sql import extract
from datetime import timedelta,datetime



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

def read_bacsis():
    return Bacsi.query.all()

def read_giokham(bs_id=None,day=None):
    giokham = Schedule.query.filter(Schedule.active.__eq__(True))
    if bs_id:
        giokham = giokham.filter(Schedule.bacsi_id.__eq__(int(bs_id)))
    if day:
        giokham=giokham.filter(Schedule.ngaykham == day)
    return giokham.order_by(extract('hour',Schedule.giobatdau)).all()

def get_schedule_by_id(schedule_id):

    return Schedule.query.get(schedule_id)


def add_appointment(giodat,khachhang_id, bacsi_id):
    a = Appointment(giodat=giodat, user_id=khachhang_id,bacsi_id= bacsi_id)

    db.session.add(a)
    db.session.commit()

def capnhattrangthaschedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    schedule.active=0
    db.session.commit()

def read_thuoc(kw=None, from_price=None, to_price = None,page=1):
    thuocs = Thuoc.query.filter(Thuoc.active.__eq__(True))
    if kw:
        thuocs = thuocs.filter(Thuoc.name.contains(kw))

    if from_price:
        thuocs = thuocs.filter(Thuoc.price.__ge__(float(from_price)))
    if to_price:
        thuocs = thuocs.filter(Thuoc.price.__le__(float(to_price)))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return thuocs.slice(start,end).all()
def count_thuocs():
    return Thuoc.query.filter(Thuoc.active.__eq__(True)).count()

