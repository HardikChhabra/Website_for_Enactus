from flask import Flask, render_template, jsonify, request
from database import engine, load_product_from_db
from sqlalchemy import text
from billing import calculate_bill_and_add_to_sheets


app = Flask(__name__)


def load_products_from_db():
  with engine.connect() as conn:
    result = conn.execute(text('select * from products'))
    PRODUCTS = []
    for row in result.all():
      PRODUCTS.append(row._mapping)
    return PRODUCTS


@app.route("/")
def hello_world():
  pr = load_products_from_db()
  return render_template('home.html', products=pr)


@app.route("/api/products")
def list_products():
  return jsonify(load_products_from_db())


@app.route("/<product>")
def show_product_detail(product):
  return jsonify(load_product_from_db(product))


@app.route("/billing")
def billing():
  pr = load_products_from_db()
  return render_template('billing.html', products=pr)


@app.route("/inventory")
def inventory():
  return render_template('inventory.html')


@app.route("/new_product")
def new():
  return render_template('new.html')


@app.route("/make_bill/apply", methods=['post'])
def make_bill():
  data = request.form
  calculate_bill_and_add_to_sheets(data)
  return jsonify(data)


if __name__ == '__main__':
  print("I am inside if")
  app.run(host='0.0.0.0', debug=True)
