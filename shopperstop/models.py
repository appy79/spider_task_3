from shopperstop import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_type=db.Column(db.String(128))
    cart = db.relationship('Product', backref='owner', lazy=True)

    def __init__(self, email, username, password,user_type):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type=user_type

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.username}{self.user_type}{self.id}"

class Product(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    cus_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sell_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(140), nullable=False)
    product_desc=db.Column(db.String, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    product_image=db.Column(db.String(20), nullable=False, default='default_profile.png')


    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"



class Cart(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Cart('{self.userid}', '{self.productid}, '{self.quantity}')"
