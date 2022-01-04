from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'IOU48FGSDFT345345@!#@$whu' #crud du lieu


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/phongmachdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

db = SQLAlchemy(app=app)