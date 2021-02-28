from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from shopperstop import db
from werkzeug.security import generate_password_hash,check_password_hash
from shopperstop.models import User, Product, Cart
from shopperstop.users.forms import RegistrationForm, LoginForm, UpdateUserForm, AddProductForm, UpdateProductForm
from shopperstop.users.picture_handler import add_profile_pic
from shopperstop.users.pro_picture_handler import add_product_pic


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    user_type=form.user_type.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')
            return redirect('index.html')
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>_cart")
@login_required
def cart_view(username):
    if current_user.user_type=='Seller':
        abort(403)
    user = User.query.filter_by(username=username).first_or_404()
    cart = Cart.query.filter_by(userid=current_user.id)
    return render_template('cart.html', cart=cart, user=user)

@users.route("/<username>_shop")
@login_required
def shop_view(username):
    if current_user.user_type=='Customer':
        abort(403)
    user=User.query.filter_by(username=username).first_or_404()
    shop=Product.query.filter_by(sell_id=current_user.id)
    return render_template('shop.html', shop=shop, user=user)


@users.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.user_type=='Customer':
        abort(403)
    form = AddProductForm()
    if form.validate_on_submit():
        product_name=form.product_name.data
        pic=add_product_pic(form.picture.data,product_name)
        product = Product(product_name=form.product_name.data,
                    product_desc=form.product_desc.data,
                    price=form.price.data,
                    quantity=form.quantity.data,
                    product_image = pic
                    )

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('add_product.html', form=form)

@users.route("/<product_id>_update", methods=['GET','POST'])
@login_required
def update_product(product_id):
    if current_user.user_type=='Customer':
        abort(403)
    product=Product.query.filter_by(id=product_id).first_or_404()


    form = UpdateProductForm()

    if form.validate_on_submit():

        if form.picture.data:
            product_name=form.product_name.data
            pic=add_product_pic(form.picture.data,product_name)
            product.product_image = pic

        product.product_name = form.product_name.data
        product.product_desc = form.product_desc.data
        product.price=form.price.data
        product.quantity=form.quantity.data
        db.session.commit()
        return redirect(url_for('users.shop_view', username=current_user.username))

    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_desc.data = product.product_desc
        form.price.data = product.price
        form.quantity.data = product.quantity

    product_image = url_for('static', filename='product_pics/' + product.product_image)

    return render_template('update_product.html', product=product, form=form)
