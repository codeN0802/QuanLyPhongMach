import sys
sys.path.append('./')

from myapp import app
from flask import render_template

# trang chủ
@app.route("/")
def home():
    return render_template("index.html")

# trang đăng ký
@app.route('/register', methods=['get', 'post'])
def user_register():
    return render_template('register.html')

# trang đăng nhập
@app.route('/login', methods=['get', 'post'])
def user_login():
    return render_template('login.html')

# trang thanh toán
@app.route('/payment', methods=['get', 'post'])
def payment():
    return render_template('payment.html',)





if __name__== "__main__":
    from myapp.admin import *
    app.run(debug=True)