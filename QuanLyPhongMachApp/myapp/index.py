# import sys
# sys.path.append('./')
from myapp import app,utils,login,mail
from flask import render_template,redirect,request,url_for,abort,Response
import cloudinary.uploader
from flask_login import login_user,logout_user, login_required,current_user
from datetime import date,datetime
import math
from flask_mail import Mail, Message
@app.route("/")
def home():
    day = request.args.get("date",date.today())
    print(day)
    bacsis = utils.read_bacsis()
    bs_id = request.args.get("bacsi_id")
    giokham = utils.read_giokham(bs_id=bs_id,day=day)
    return render_template("index.html",bacsis=bacsis,giokham=giokham)

@app.route("/register", methods=['get','post'])
def user_register():
    err_msg= ""
    if request.method.__eq__("POST"): #POST PHẢI IN HOA
        name = request.form.get("name")
        email = request.form.get('email')
        sdt = request.form.get('sdt')
        username = request.form.get("username")
        pasword = request.form.get("password")
        confirm = request.form.get("confirm")

        try:
            if pasword.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res= cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                msg = Message('BÁC SĨ GIA ĐÌNH', sender='nghinguyen08022000@gmail.com',
                              recipients=[email])
                msg.body = "Cám ơn bạn đã đăng ký tài khoản"
                mail.send(msg)
                utils.add_user(name=name, email=email, sdt=sdt,username=username, pasword=pasword, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = "Mật khẩu không khớp"
        except :
                db.session.rollback() #sqlalchemy.exc.PendingRollbackError
                err_msg = "Username hoặc Email đã có trên hệ thống"
    if current_user.is_authenticated: # chặn đã đăng nhập không được vô login
        return redirect(url_for('home'))
    return render_template("register.html", err_msg=err_msg)

@app.route("/login", methods=['get','post'])
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get("username")
        pasword = request.form.get("password")
        user = utils.check_login(username=username,pasword=pasword)
        if user:
            login_user(user=user) #ghi nnhaan trang thai da dang nhap

            # next = request.args.get('next', 'home')
            return redirect(url_for('home'))
        else:
            err_msg = "Vui lòng kiểm tra lại Username và Password"
    if current_user.is_authenticated: # chặn đã đăng nhập không được vô login
        return redirect(url_for('home'))
    return render_template("login.html",err_msg=err_msg)



@app.route("/logout")
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@app.route("/admin-login", methods=['post'])
def admin_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get("username")
        pasword = request.form.get("password")
        user = utils.check_adminlogin(username=username,pasword=pasword)
        if user:
            login_user(user=user)  # ghi nnhaan trang thai da dang nhap
            return redirect('/admin')
        else:
            err_msg ="Vui lòng kiểm tra lại Username hoặc Password"
            return  abort(Response(err_msg))


@app.route("/booking/<int:schedule_id>")
def shedule_detail(schedule_id):
    booking = utils.get_schedule_by_id(schedule_id)


    return render_template("payment.html", booking=booking)

@app.route('/booking/<int:schedule_id>',methods=['get','post'])
@login_required
def bookingappointment(schedule_id):
    err_msg=''
    booking = utils.get_schedule_by_id(schedule_id)
    if request.method.__eq__("POST"):
        giodat= booking.giobatdau
        bacsi_id = booking.bacsi.id
        khachhang_id=current_user.id
        if booking.active == 1:
            utils.add_appointment(giodat=giodat, khachhang_id=khachhang_id, bacsi_id=bacsi_id)
            utils.capnhattrangthaschedule(schedule_id=schedule_id)
            msg = Message('BÁC SĨ GIA ĐÌNH', sender='nghinguyen08022000@gmail.com',
                          recipients=[current_user.email])
            msg.html = render_template("email.html",booking = utils.get_schedule_by_id(schedule_id) )
            mail.send(msg)
            return redirect(url_for('home'))
        else:
            err_msg='Lịch đã có người đặt'
    return render_template("payment.html", booking=booking,err_msg=err_msg)

@app.route("/thuoc")
def thuoc():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    page = request.args.get("page", 1)
    thuocs = utils.read_thuoc(kw=kw,from_price=from_price,to_price=to_price,page=int(page))
    counter= utils.count_thuocs()

    return render_template("thuoc.html",thuocs=thuocs ,pages=math.ceil(counter/app.config['PAGE_SIZE']))

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__== "__main__":
    from myapp.admin import *
    app.run(debug=True)