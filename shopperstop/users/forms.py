from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, IntegerField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from wtforms_validators import AlphaNumeric
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from shopperstop.models import User, Product




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired(), AlphaNumeric()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!'), Length(min=6, max=30, message='Password should be between 6 and 30 characters long'), AlphaNumeric()] )
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    user_type=RadioField('User Type', choices=['Customer', 'Seller'], validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email has been registered')

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('Username has been registered')


class AddProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_desc = TextAreaField('Product Description', validators=[DataRequired()])
    price= IntegerField('Price', validators=[DataRequired()])
    quantity= IntegerField('Quantity', validators=[DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Item')


class UpdateProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_desc = TextAreaField('Product Description', validators=[DataRequired()])
    price= IntegerField('Price', validators=[DataRequired()])
    quantity= IntegerField('Quantity', validators=[DataRequired()])
    picture = FileField('Update Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Item')

class QuantityForm(FlaskForm):
    quantity=IntegerField('Quantity', validators=[DataRequired()])
    submit=SubmitField('Add to cart')

class QuantityEdit(FlaskForm):
    quantity=IntegerField('Quantity', validators=[DataRequired()])
    submit=SubmitField('Change quantity')

class OrderForm(FlaskForm):
    name=StringField('Receiver Name', validators=[DataRequired()])
    address=TextAreaField('Address', validators=[DataRequired()])
    phone=StringField('Phone Number', validators=[DataRequired()])
    submit=SubmitField('Checkout')
