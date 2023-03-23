from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_product_from_db(product):
  with engine.connect() as conn:
    str = f'select * from products where product = "{product}"'
    result = conn.execute(text(str))
    row = result.all()
    if len(row) == 0:
      return None
    else:
      pro = row[0]._mapping
      return dict(pro)


def load_price_from_db():
  with engine.connect() as conn:
    result = conn.execute(text('select * from products'))
    PRICES = []
    for row in result.all():
      PRICES.append(row._mapping)
    return PRICES
