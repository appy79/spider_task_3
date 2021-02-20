from flask import render_template,request,Blueprint
from shopperstop.models import Product

core = Blueprint('core',__name__)

@core.route('/')
def index():
    products = Product.query.order_by(Product.id.asc())
    return render_template('index.html',products=products)

@core.route('/info')
def info():
    return render_template('info.html')
