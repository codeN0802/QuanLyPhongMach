# import sys
# sys.path.append('./')
from myapp import app,utils,login
from flask import render_template,redirect,request,url_for,abort,Response
import cloudinary.uploader
from flask_login import login_user,logout_user, login_required,current_user

@app.route("/")
def home():
    return render_template("index.html")

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

                # msg = Message('Vy Nguyễn Homewear', sender='nghinguyen08022000@gmail.com',
                #               recipients=[email])
                # msg.body = "Cám ơn bạn đã đăng ký tài khoản"
                # mail.send(msg)
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

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__== "__main__":
    from myapp.admin import *
    app.run(debug=True)