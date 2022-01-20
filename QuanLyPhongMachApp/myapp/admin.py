from myapp import app,db
from myapp.models import *
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect,request
from flask_login import logout_user,current_user
import myapp
admin = Admin(app=app, name='Quản trị phòng mạch ',template_mode='bootstrap4')

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class Logoutview(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class ThuocView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'price', 'description']
    column_filters = ['name', 'price', 'description']
    column_exclude_list = ['image', 'active']
    column_labels = {
        'name' : 'Tên thuốc',
        'description' : 'Mô tả',
        'price' : 'Gía',
        'soluong': 'Số lượng',
        'created_date' : 'Ngày tạo'
    }

class UserView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'sdt', 'username']
    column_filters = ['name', 'sdt', 'username']
    column_exclude_list = ['avatar', 'acive']
    column_labels = {
        'name' : 'Họ và tên',
        'email' : 'Email',
        'sdt' : 'Phone',
        'username': 'Tài khoản',
        'pasword' : 'Mật khẩu',
        'created_date' : 'Ngày tạo'
    }

class BacsiView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {
        'user_id' : 'Họ và tên Bác sĩ'}


class ScheduleView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['ngaykham', 'giobatdau', 'gioketthuc']
    column_filters = ['ngaykham', 'giobatdau', 'gioketthuc']
    column_exclude_list = ['active']
    column_labels = {
        'created_date' : 'Ngày tạo',
        'ngaykham' : 'Ngày khám',
        'giobatdau' : 'Giờ bắt đầu',
        'gioketthuc' : 'Giờ kết thúc',
        'bacsi_id' : 'Id bác sĩ'
    }


admin.add_view(AuthenticatedModelView(Category,db.session))
admin.add_view(AuthenticatedModelView(Thuoc,db.session, name='Thuốc'))
admin.add_view(AuthenticatedModelView(User,db.session))
admin.add_view(AuthenticatedModelView(Bacsi,db.session, name='Bác sĩ'))
admin.add_view(AuthenticatedModelView(Khachhang,db.session,name='Khách hàng'))
admin.add_view(AuthenticatedModelView(Schedule,db.session, name='Lịch khám'))
admin.add_view(AuthenticatedModelView(Appointment,db.session, name='Appointment'))
admin.add_view(AuthenticatedModelView(AppointmentDetail,db.session,name='Chi tiết đơn hàng'))
admin.add_view(Logoutview(name='Đăng xuất'))