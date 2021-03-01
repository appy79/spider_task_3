from flask import render_template,request,Blueprint
from shopperstop.models import Product
from shopperstop.users.forms import QuantityForm

core = Blueprint('core',__name__)

@core.route('/')
def index():
    products = Product.query.order_by(Product.id.desc())
    form=QuantityForm()
    return render_template('index.html',products=products, form=form)

@core.route('/info')
def info():
    return render_template('info.html')
