from sqlalchemy import Column,Integer,ForeignKey,Boolean,DateTime,String,Enum,Float,Date
from sqlalchemy.orm import relationship
from myapp import db
from datetime import datetime
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    BACSI = 2
    KHACHHANG = 3
    YTA = 4

    def __str__(self):
        return self.name

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100),nullable=False,unique=True)
    sdt = Column(String(50),nullable=False)
    username = Column(String(255),nullable=False,unique=True)
    pasword = Column(String(255),nullable=False)
    avatar = Column(String(255))
    acive = Column(Boolean,default=True)
    created_date = Column(DateTime,default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.KHACHHANG)
    bacsi_profiles = relationship('Bacsi', uselist=False, backref='user')
    khachhang_profiles = relationship('Khachhang', uselist=False, backref='user')

    def __str__(self):
        return self.name

class Bacsi(db.Model):
    __tablename__ = 'bacsi'
    id = Column(Integer,primary_key=True,autoincrement=True)

    user_id = Column(Integer,ForeignKey('user.id'),unique=True)

    schedules = relationship('Schedule', backref='bacsi',lazy=True)
    appoints = relationship('Appointment',backref='bacsi',lazy=True)



class Khachhang(db.Model):
    __tablename__ = 'khachhang'
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.id'),unique=True)
    appoints = relationship('Appointment', backref='khachhang', lazy=True)

class Schedule(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date= Column(DateTime,default=datetime.now())
    ngaykham = Column(Date)
    giobatdau = Column(DateTime)
    gioketthuc = Column(DateTime)
    active = Column(Boolean,default=True)
    bacsi_id = Column(Integer,ForeignKey('bacsi.id'),nullable=False)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50),nullable=False,unique=True)
    thuocs = relationship('Thuoc', backref ='category',lazy=True)

    def __str__(self):
        return self.name




class Thuoc(BaseModel):
    __tablename__ = 'thuoc'

    name = Column(String(50),nullable=False,unique=True)
    description = Column(String(255))
    price = Column(Float,default=0)
    soluong = Column(Float,default=0)
    image = Column(String(255))
    active = Column(Boolean,default=True)
    created_date = Column(DateTime,default=datetime.now())
    category_id = Column(Integer,ForeignKey('category.id'),nullable=False)
    details = relationship('AppointmentDetail', backref='thuoc', lazy=True)

    def __str__(self):
        return self.name

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean)
    is_thanhtoan = Column(Boolean)
    giodat = Column(DateTime)
    khachhang_id = Column(Integer,ForeignKey('khachhang.id'),nullable=False)
    bacsi_id = Column(Integer,ForeignKey('bacsi.id'),nullable=False)
    details = relationship('AppointmentDetail',backref='appointment',lazy=True)

class AppointmentDetail(db.Model):
    appoint_id = Column(Integer,ForeignKey('appointment.id'),nullable=False,primary_key=True)
    thuoc_id = Column(Integer,ForeignKey(Thuoc.id),nullable=False,primary_key=True)
    quantity = Column(Integer,default=0)
    amount = Column(Float,default=0)

if __name__ == '__main__':
    db.create_all()