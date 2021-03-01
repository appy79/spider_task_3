from shopperstop import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user


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

    def __init__(self, email, username, password,user_type):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type=user_type

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.email},{self.username},{self.user_type}"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sell_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(140), nullable=False)
    product_desc=db.Column(db.String, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    price=db.Column(db.Integer, nullable=False)
    product_image=db.Column(db.String(20), nullable=False, default='default_profile.png')


    def __init__(self, product_name, product_desc, quantity, price, product_image):
        self.product_name = product_name
        self.product_desc = product_desc
        self.quantity = quantity
        self.price = price
        self.product_image=product_image
        self.sell_id = current_user.id


    def __repr__(self):
        return f"Product : {self.id}, {self.product_name}, {self.product_desc}, {self.price}, {self.sell_id}"



class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    prod=db.relationship("Product", backref="prod", lazy=True)

    def __repr__(self):
        return f"Cart('{self.userid}', '{self.productid}, '{self.quantity}')"

class Order(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_date}','{self.total_price}','{self.userid}'')"

class OrderedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.id'), nullable=False)
    productid = db.Column(db.Integer,db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.orderid}','{self.productid}','{self.quantity}')"
