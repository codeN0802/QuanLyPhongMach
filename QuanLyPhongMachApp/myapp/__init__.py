from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = 'IOU48FGSDFT345345@!#@$whu' #crud du lieu


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/phongmachdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

db = SQLAlchemy(app=app)

cloudinary.config(
  cloud_name = "dn8gvatsu",
  api_key = "932217124943281",
  api_secret = "jxg3UHnXKjzZqG_sUtTON7DmDr0"
)

login = LoginManager(app=app)