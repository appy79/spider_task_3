from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from shopperstop import db
from werkzeug.security import generate_password_hash,check_password_hash
from shopperstop.models import User, Product, Cart, Order, OrderedProduct
from shopperstop.users.forms import RegistrationForm, LoginForm, UpdateUserForm, AddProductForm, UpdateProductForm, QuantityForm, QuantityEdit, OrderForm
from shopperstop.users.picture_handler import add_profile_pic
from shopperstop.users.pro_picture_handler import add_product_pic


users = Blueprint('users', __name__)

#REGISTER
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


#LOGIN
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            name=user.username
            if user.user_type=='Customer':
                dash=name+'_cart'
            else:
                dash=name+'_shop'
            return redirect(dash)
    return render_template('login.html', form=form)



#LOGOUT
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))



#UPDATE_USER
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


total=0
#CART DISPLAY
@users.route("/<username>_cart")
@login_required
def cart_view(username):
    if current_user.user_type=='Seller':
        abort(403)
    oform=OrderForm()
    qform=QuantityEdit()
    user = User.query.filter_by(username=username).first_or_404()
    cart = Cart.query.filter_by(userid=current_user.id).all()
    global total
    for product in cart:
        total+=product.prod.price*product.quantity
    return render_template('cart.html', cart=cart, user=user, total=total, qform=qform, oform=oform)


#EDITING CART
@users.route("/<product_id>_cart_edit", methods=['POST','GET'])
@login_required
def cart_edit(product_id):
    if current_user.user_type=='Seller':
        abort(403)
    editpro=Cart.query.filter_by(userid=current_user.id, productid=product_id).first()
    qform=QuantityEdit()
    if qform.validate_on_submit():
        editpro.quantity=qform.quantity.data
        db.session.commit()
        return redirect(url_for('users.cart_view', username=current_user.username))



#SHOP OF MERCHANT
@users.route("/<username>_shop")
@login_required
def shop_view(username):
    if current_user.user_type=='Customer':
        abort(403)
    user=User.query.filter_by(username=username).first_or_404()
    shop=Product.query.filter_by(sell_id=current_user.id)
    return render_template('shop.html', shop=shop, user=user)



#ADDING A PRODUCT
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


#UPDATING A PRODUCT
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



#DELETING A PRODUCT
@users.route('/<product_id>_delete')
@login_required
def delete_product(product_id):
    product=Product.query.filter_by(id=product_id).first_or_404()
    if product.sell_id != current_user.id:
        abort(403)
    product.quantity=0
    db.session.commit()
    return redirect(url_for('users.shop_view', username=current_user.username))


#ADD TO CART
@users.route('/<product_id>_cart',methods=['GET','POST'])
@login_required
def add_to_cart(product_id):
    if current_user.user_type=='Seller':
        abort(403)
    product=Product.query.filter_by(id=product_id).first_or_404()
    exists=Cart.query.filter_by(productid=product_id, userid=current_user.id).first()
    form=QuantityForm()
    if form.validate_on_submit():
        if exists:
            exists.quantity+=form.quantity.data
        else:
            cart=Cart(userid=current_user.id,
                        productid=product_id,
                        quantity=form.quantity.data)
            db.session.add(cart)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('index.html', form=form)


#CHECKOUT
@users.route('/checkout', methods=['GET','POST'])
@login_required
def checkout():
    if current_user.user_type=='Seller':
        abort(403)
    qr=Cart.query.filter_by(userid=current_user.id).first()
    pro=Product.query.filter_by(id=qr.productid).first()
    oform=OrderForm()
    global total
    if oform.validate_on_submit():
        order=Order(total_price=total,
                    name=oform.name.data,
                    address=oform.address.data,
                    phone=oform.phone.data,
                    sell_id=pro.sell_id)
        db.session.add(order)
        db.session.commit()
        prod=Cart.query.filter_by(userid=current_user.id).all()
        last_order=Order.query.filter_by(userid=current_user.id).first()
        for pr in prod:
            dec=Product.query.filter_by(id=pr.productid).first()
            dec.quantity-=pr.quantity
            ordproduct=OrderedProduct(orderid=last_order.id,
                                    productid=pr.productid,
                                    quantity=pr.quantity)
            db.session.add(ordproduct)
            db.session.delete(pr)
            db.session.commit()
        total=0
        return redirect(url_for('core.index'))


#CUSTOMER HISTORY
@users.route('/<username>_purchase_history')
@login_required
def cust_history(username):
    if current_user.user_type=='Seller':
        abort(403)

    orders=Order.query.filter_by().all()
    return render_template('cust_history.html')


#SELLER HISTORY
@users.route('/<username>_sell_history')
@login_required
def sell_history(username):
    if current_user.user_type=='Customer':
        abort(403)
    orders=Order.query.filter_by(sell_id=current_user.id).all()
    return render_template('sell_history.html', orders=orders)
