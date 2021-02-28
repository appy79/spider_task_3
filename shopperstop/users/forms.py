from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from shopperstop.models import User, Product




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
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
